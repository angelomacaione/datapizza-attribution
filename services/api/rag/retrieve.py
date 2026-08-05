"""
Retrieval ibrido: BM25 lessicale + denso multilingue, fusi con RRF.

Perche' ibrido. Il denso da solo perde i codici prodotto e le cifre: "K1-08" e
"K1-03" hanno quasi lo stesso vettore, e per questa demo la differenza tra i due
e' tutto. BM25 da solo perde la parafrasi: chi chiede "quanto costa noleggiare
un robot" non scrive "rental" ne' "cauzione". Servono entrambi.

La fusione e' Reciprocal Rank Fusion: lavora sui ranghi e non sui punteggi, che
sono su scale incomparabili (coseno in [-1,1] contro BM25 non normalizzato).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from datapizza.type import Chunk
from rank_bm25 import BM25Okapi

from .embedder import LocalEmbedder
from .store import NumpyVectorstore

RRF_K = 10          # su 221 chunk il 60 canonico appiattisce tutto: i primi
                    # dieci risultati escono con lo stesso punteggio e l'ordine
                    # diventa arbitrario. Con K piu' basso la testa si separa.
DENSE_POOL = 20     # quanti candidati prende ciascun ramo prima della fusione.
LEXICAL_POOL = 20   # 40 su 221 significava pescare il 18% del corpus a ogni
                    # domanda: troppa spazzatura entra in fusione.


def _tokenize(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    # teniamo attaccati i codici tipo k1-08 e le cifre con separatori
    return re.findall(r"[a-z0-9]+(?:[-_.][a-z0-9]+)*", text)


@dataclass
class Hit:
    chunk: Chunk
    score: float
    dense_rank: int | None
    lexical_rank: int | None
    why: str          # spiegazione leggibile di come e' stato pescato


class HybridRetriever:
    def __init__(self, store: NumpyVectorstore, embedder: LocalEmbedder,
                 collection: str = "prometeo"):
        self.store = store
        self.embedder = embedder
        self.collection = collection
        self._chunks = store.all_chunks(collection)
        self._bm25 = BM25Okapi([_tokenize(c.text) for c in self._chunks]) if self._chunks else None
        self._by_id = {c.id: c for c in self._chunks}

    def search(self, query: str, k: int = 8, *,
               channels: list[str] | None = None,
               registers: list[str] | None = None) -> list[Hit]:
        if not self._chunks:
            return []

        dense = self.store.search(self.collection, self.embedder.embed_query(query),
                                  k=DENSE_POOL)
        dense_rank = {c.id: i for i, c in enumerate(dense)}

        scores = self._bm25.get_scores(_tokenize(query))
        top = sorted(range(len(scores)), key=lambda i: -scores[i])[:LEXICAL_POOL]
        lex_rank = {self._chunks[i].id: r for r, i in enumerate(top) if scores[i] > 0}

        fused: dict[str, float] = {}
        for cid, r in dense_rank.items():
            fused[cid] = fused.get(cid, 0.0) + 1.0 / (RRF_K + r + 1)
        for cid, r in lex_rank.items():
            fused[cid] = fused.get(cid, 0.0) + 1.0 / (RRF_K + r + 1)

        hits: list[Hit] = []
        for cid, s in sorted(fused.items(), key=lambda kv: -kv[1]):
            c = self._by_id.get(cid)
            if c is None:
                continue
            meta = c.metadata or {}
            if channels and meta.get("channel") not in channels:
                continue
            if registers and meta.get("register") not in registers:
                continue
            d, l = dense_rank.get(cid), lex_rank.get(cid)
            if d is not None and l is not None:
                why = f"both (denso #{d + 1}, lessicale #{l + 1})"
            elif d is not None:
                why = f"solo semantico (#{d + 1})"
            else:
                why = f"solo lessicale (#{l + 1})"
            hits.append(Hit(chunk=c, score=s, dense_rank=d, lexical_rank=l, why=why))
            if len(hits) >= k:
                break
        return hits
