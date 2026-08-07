#!/usr/bin/env python3
"""
Costruisce l'indice a partire dal vault. Gira offline, non serve al runtime.

    python3 scripts/build_index.py

Produce in `index/`:
    prometeo.chunks.json    i chunk con i metadati (versionabile, e' piccolo)
    prometeo.vectors.npy    gli embedding (rigenerabili: fuori dal git)
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services" / "api"))

from datapizza.type import Chunk as DPChunk  # noqa: E402
from rag.chunker import chunk_vault  # noqa: E402
from rag.embedder import LocalEmbedder  # noqa: E402
from rag.embedder_offline import TfidfEmbedder  # noqa: E402
from rag.store import NumpyVectorstore, DEFAULT_COLLECTION  # noqa: E402

VAULT = ROOT / "corpus" / "prometeo-cup"
OUT = ROOT / "index"


def pick_embedder(texts: list[str]):
    """e5 se il modello e' raggiungibile, altrimenti il ripiego offline.

    Non e' una comodita': ci sono ambienti che bloccano HuggingFace, e in quel
    caso vogliamo che la catena giri lo stesso invece di morire in fase di
    build. Quale dei due sia stato usato finisce in build-info.json, cosi' non
    resta ambiguo cosa c'e' dentro l'indice.
    """
    # Se e' configurato un fornitore remoto, e' quello che comanda: l'indice
    # DEVE nascere dallo stesso modello che poi interroghera' la produzione.
    fornitore = os.environ.get("EMBEDDING_PROVIDER", "").lower()
    if fornitore in ("voyage", "openai"):
        from rag.embedder_api import ApiEmbedder
        emb = ApiEmbedder(fornitore)
        emb.embed("prova di raggiungibilita'")
        return emb, emb.model_name

    force = os.environ.get("EMBEDDER", "").lower()
    if force != "tfidf":
        try:
            emb = LocalEmbedder()
            emb.embed("prova di raggiungibilita' del modello")
            return emb, "e5"
        except Exception as exc:  # rete bloccata, disco pieno, modello assente
            if force == "e5":
                raise
            print(f"!  e5 non disponibile ({type(exc).__name__}), passo al ripiego TF-IDF")
    emb = TfidfEmbedder().fit(texts)
    return emb, "tfidf"


def main() -> int:
    t0 = time.time()
    print(f"vault:  {VAULT}")
    chunks = chunk_vault(VAULT)
    print(f"chunk:  {len(chunks)}")

    embedder, kind = pick_embedder([c.text for c in chunks])
    print(f"modello: {embedder.model_name} (dim {embedder.dimensions})")
    vectors = embedder.embed_passages([c.text for c in chunks])
    print(f"embedding calcolati in {time.time() - t0:.1f}s")

    dp_chunks = [
        DPChunk(
            id=c.id,
            text=c.text,
            embeddings=[embedder.as_dense(v)],
            metadata={k: val for k, val in c.to_dict().items() if k not in ("id", "text")}
            | {"citation": c.citation()},
        )
        for c, v in zip(chunks, vectors)
    ]

    store = NumpyVectorstore()
    store.add(dp_chunks)
    OUT.mkdir(exist_ok=True)
    store.save(OUT)
    if kind == "tfidf":
        embedder.save(OUT)

    (OUT / "build-info.json").write_text(json.dumps({
        "chunks": len(chunks),
        "model": embedder.model_name,
        "embedder_kind": kind,
        "dimensions": embedder.dimensions,
        "collection": DEFAULT_COLLECTION,
        "channels": sorted({c.channel for c in chunks}),
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"scritto in {OUT} — totale {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
