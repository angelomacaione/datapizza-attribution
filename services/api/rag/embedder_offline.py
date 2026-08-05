"""
Embedder di ripiego che non scarica nulla.

Serve in due casi reali: ambienti senza accesso a HuggingFace (il container in
cui e' stata sviluppata questa demo lo blocca) e chiunque voglia far girare il
progetto senza aspettare 2 GB di modello.

E' TF-IDF + SVD (analisi semantica latente): cattura la co-occorrenza, non la
semantica vera. Sulla parafrasi lontana perde contro e5, sui nomi e sui codici
tiene benissimo. Va bene per sviluppare e testare la catena; per la demo vera
usare `LocalEmbedder`.

Differenza pratica da tenere a mente: questo va ADDESTRATO sul corpus prima di
poter vettorializzare, mentre e5 e' pre-addestrato. Da qui `fit()`.
"""

from __future__ import annotations

import pickle
import re
import unicodedata
from pathlib import Path

import numpy as np
from datapizza.core.embedder import BaseEmbedder
from datapizza.type import DenseEmbedding
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer


def _analyzer(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    toks = re.findall(r"[a-z0-9]+(?:[-_.][a-z0-9]+)*", text)
    return toks + [f"{a}_{b}" for a, b in zip(toks, toks[1:])]


class TfidfEmbedder(BaseEmbedder):
    model_name = "tfidf-svd-locale"

    def __init__(self, dimensions: int = 256, embedding_name: str = "dense"):
        self._dimensions = dimensions
        self.embedding_name = embedding_name
        self._pipe = None

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def fit(self, texts: list[str]) -> "TfidfEmbedder":
        n = max(2, min(self._dimensions, len(texts) - 1))
        self._dimensions = n
        self._pipe = make_pipeline(
            TfidfVectorizer(analyzer=_analyzer, sublinear_tf=True, min_df=1),
            TruncatedSVD(n_components=n, random_state=0),
            Normalizer(copy=False),
        )
        self._pipe.fit(texts)
        return self

    def embed(self, text: str | list[str], **kwargs):
        if self._pipe is None:
            raise RuntimeError("TfidfEmbedder non addestrato: chiama fit() sul corpus")
        single = isinstance(text, str)
        matrix = self._pipe.transform([text] if single else text)
        vectors = np.asarray(matrix, dtype=np.float32)
        return vectors[0].tolist() if single else [v.tolist() for v in vectors]

    async def a_embed(self, text: str | list[str], **kwargs):
        return self.embed(text, **kwargs)

    def embed_query(self, text: str) -> list[float]:
        return self.embed(text)

    def embed_passages(self, texts: list[str]) -> list[list[float]]:
        return self.embed(texts)

    def as_dense(self, vector: list[float]) -> DenseEmbedding:
        return DenseEmbedding(name=self.embedding_name, vector=vector)

    # ---- persistenza ------------------------------------------------------

    def save(self, directory: str | Path):
        d = Path(directory)
        d.mkdir(parents=True, exist_ok=True)
        with open(d / "tfidf.pkl", "wb") as fh:
            pickle.dump({"pipe": self._pipe, "dim": self._dimensions}, fh)

    @classmethod
    def load(cls, directory: str | Path) -> "TfidfEmbedder":
        with open(Path(directory) / "tfidf.pkl", "rb") as fh:
            blob = pickle.load(fh)
        obj = cls(dimensions=blob["dim"])
        obj._pipe = blob["pipe"]
        return obj
