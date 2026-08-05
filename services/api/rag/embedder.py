"""
Embedder locale che implementa l'interfaccia di datapizza-ai.

Nel loro ecosistema esistono solo `embedders-openai` e `embedders-google`:
entrambi vogliono una chiave e fanno pagare a token. Il corpus qui e' di 23.000
parole, non ha senso spedirlo fuori. `BaseEmbedder` chiede un solo metodo
astratto (`embed`), quindi ci si innesta scrivendo poche righe e restando
componenti di pipeline a tutti gli effetti.
"""

from __future__ import annotations

import threading
from typing import Iterable

from datapizza.core.embedder import BaseEmbedder
from datapizza.type import DenseEmbedding

# e5 e' addestrato per il retrieval e vuole i prefissi: senza, la qualita' cala
# parecchio. Sono asimmetrici di proposito, query e passaggio non sono la stessa
# cosa.
QUERY_PREFIX = "query: "
PASSAGE_PREFIX = "passage: "

DEFAULT_MODEL = "intfloat/multilingual-e5-large"


class LocalEmbedder(BaseEmbedder):
    """Embedding multilingue in-process, via fastembed (ONNX, niente torch)."""

    def __init__(self, model_name: str = DEFAULT_MODEL, embedding_name: str | None = None):
        self.model_name = model_name
        self.embedding_name = embedding_name or "dense"
        self._model = None
        self._lock = threading.Lock()

    # il modello pesa: caricalo alla prima richiesta, non all'import
    def _ensure(self):
        if self._model is None:
            with self._lock:
                if self._model is None:
                    from fastembed import TextEmbedding
                    self._model = TextEmbedding(self.model_name)
        return self._model

    @property
    def dimensions(self) -> int:
        from fastembed import TextEmbedding
        for m in TextEmbedding.list_supported_models():
            if m["model"] == self.model_name:
                return int(m["dim"])
        raise ValueError(f"modello sconosciuto: {self.model_name}")

    def _encode(self, texts: Iterable[str]) -> list[list[float]]:
        model = self._ensure()
        return [v.tolist() for v in model.embed(list(texts))]

    # ---- interfaccia datapizza -------------------------------------------

    def embed(self, text: str | list[str], **kwargs) -> list[float] | list[list[float]]:
        is_query = bool(kwargs.get("is_query", False))
        prefix = QUERY_PREFIX if is_query else PASSAGE_PREFIX
        if isinstance(text, str):
            return self._encode([prefix + text])[0]
        return self._encode([prefix + t for t in text])

    async def a_embed(self, text: str | list[str], **kwargs):
        return self.embed(text, **kwargs)

    # ---- comodita' --------------------------------------------------------

    def embed_query(self, text: str) -> list[float]:
        return self.embed(text, is_query=True)  # type: ignore[return-value]

    def embed_passages(self, texts: list[str]) -> list[list[float]]:
        return self.embed(texts, is_query=False)  # type: ignore[return-value]

    def as_dense(self, vector: list[float]) -> DenseEmbedding:
        return DenseEmbedding(name=self.embedding_name, vector=vector)
