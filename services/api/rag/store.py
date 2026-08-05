"""
Vector store in memoria che implementa l'interfaccia `Vectorstore` di
datapizza-ai.

Con 221 chunk un array numpy e' piu' veloce di Qdrant e non ha niente da
amministrare. Implementando la loro classe astratta pero' resta innestabile
nella loro pipeline esattamente come Qdrant: se un giorno il corpus cresce, si
sostituisce il componente senza toccare il resto.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from datapizza.core.vectorstore import Vectorstore
from datapizza.type import Chunk, DenseEmbedding

DEFAULT_COLLECTION = "prometeo"


def _cosine(matrix: np.ndarray, vector: np.ndarray) -> np.ndarray:
    """Similarita' coseno di un vettore contro tutte le righe."""
    if matrix.size == 0:
        return np.zeros(0, dtype=np.float32)
    denom = (np.linalg.norm(matrix, axis=1) * np.linalg.norm(vector)) + 1e-10
    return (matrix @ vector) / denom


class NumpyVectorstore(Vectorstore):
    """Store denso in memoria, persistibile su disco in npz + json."""

    def __init__(self, collection_name: str = DEFAULT_COLLECTION,
                 embedding_name: str = "dense"):
        self.collection_name = collection_name
        self.embedding_name = embedding_name
        self._chunks: dict[str, list[Chunk]] = {}
        self._matrix: dict[str, np.ndarray] = {}

    # ---- interfaccia datapizza -------------------------------------------

    def add(self, chunk: Chunk | list[Chunk], collection_name: str | None = None):
        name = collection_name or self.collection_name
        items = chunk if isinstance(chunk, list) else [chunk]
        bucket = self._chunks.setdefault(name, [])
        vectors = []
        for c in items:
            vec = self._vector_of(c)
            if vec is None:
                raise ValueError(f"chunk {c.id} senza embedding: indicizzalo prima")
            bucket.append(c)
            vectors.append(vec)
        new = np.asarray(vectors, dtype=np.float32)
        cur = self._matrix.get(name)
        self._matrix[name] = new if cur is None else np.vstack([cur, new])

    async def a_add(self, chunk: Chunk | list[Chunk], collection_name: str | None = None):
        return self.add(chunk, collection_name)

    def search(self, collection_name: str, query_vector: list[float], k: int = 10,
               vector_name: str | None = None, **kwargs) -> list[Chunk]:
        name = collection_name or self.collection_name
        matrix = self._matrix.get(name)
        bucket = self._chunks.get(name, [])
        if matrix is None or not bucket:
            return []
        scores = _cosine(matrix, np.asarray(query_vector, dtype=np.float32))
        order = np.argsort(-scores)[:k]
        out = []
        for i in order:
            c = bucket[int(i)]
            c.metadata = {**(c.metadata or {}), "score": float(scores[int(i)])}
            out.append(c)
        return out

    async def a_search(self, collection_name: str, query_vector: list[float], k: int = 10,
                       vector_name: str | None = None, **kwargs) -> list[Chunk]:
        return self.search(collection_name, query_vector, k, vector_name, **kwargs)

    def retrieve(self, collection_name: str, ids: list[str], **kwargs) -> list[Chunk]:
        wanted = set(ids)
        return [c for c in self._chunks.get(collection_name or self.collection_name, [])
                if c.id in wanted]

    def remove(self, collection_name: str, ids: list[str], **kwargs):
        name = collection_name or self.collection_name
        bucket = self._chunks.get(name, [])
        keep = [i for i, c in enumerate(bucket) if c.id not in set(ids)]
        self._chunks[name] = [bucket[i] for i in keep]
        if name in self._matrix and len(self._matrix[name]):
            self._matrix[name] = self._matrix[name][keep]

    def update(self, collection_name: str, payload: dict, points: list[int], **kwargs):
        bucket = self._chunks.get(collection_name or self.collection_name, [])
        for p in points:
            if 0 <= p < len(bucket):
                bucket[p].metadata = {**(bucket[p].metadata or {}), **payload}

    # ---- interne ----------------------------------------------------------

    def _vector_of(self, c: Chunk) -> list[float] | None:
        for e in (c.embeddings or []):
            if isinstance(e, DenseEmbedding) and e.name == self.embedding_name:
                return e.vector
        for e in (c.embeddings or []):
            if isinstance(e, DenseEmbedding):
                return e.vector
        return None

    def all_chunks(self, collection_name: str | None = None) -> list[Chunk]:
        return list(self._chunks.get(collection_name or self.collection_name, []))

    # ---- persistenza ------------------------------------------------------

    def save(self, directory: str | Path, collection_name: str | None = None):
        name = collection_name or self.collection_name
        d = Path(directory)
        d.mkdir(parents=True, exist_ok=True)
        np.save(d / f"{name}.vectors.npy", self._matrix.get(name, np.zeros((0, 0), np.float32)))
        payload = [{"id": c.id, "text": c.text, "metadata": c.metadata}
                   for c in self._chunks.get(name, [])]
        (d / f"{name}.chunks.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    @classmethod
    def load(cls, directory: str | Path, collection_name: str = DEFAULT_COLLECTION,
             embedding_name: str = "dense") -> "NumpyVectorstore":
        d = Path(directory)
        store = cls(collection_name=collection_name, embedding_name=embedding_name)
        matrix = np.load(d / f"{collection_name}.vectors.npy")
        payload = json.loads((d / f"{collection_name}.chunks.json").read_text(encoding="utf-8"))
        chunks = []
        for row, vec in zip(payload, matrix):
            chunks.append(Chunk(id=row["id"], text=row["text"],
                                embeddings=[DenseEmbedding(name=embedding_name,
                                                           vector=vec.tolist())],
                                metadata=row["metadata"]))
        store._chunks[collection_name] = chunks
        store._matrix[collection_name] = matrix.astype(np.float32)
        return store
