#!/usr/bin/env python3
"""
Misura il retrieval sull'indice vero, usando vettori di domanda precalcolati.

    python3 scripts/eval_retrieval.py [cartella_indice]

Non carica il modello: legge i vettori delle domande da index/probe-queries.json.
Cosi' gira anche dove HuggingFace non e' raggiungibile.

Oltre ai primi risultati stampa due margini, che servono a capire se il sistema
sa distinguere "ho trovato" da "non c'e' niente":
  margine testa-coda  quanto il primo stacca il decimo
  coseno massimo      il migliore in assoluto sul ramo denso
Sulle domande fuori corpus questi due devono crollare. Se non crollano, il
livello "fuori corpus" non e' rilevabile e va ripensato.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services" / "api"))

from rag.retrieve import HybridRetriever  # noqa: E402
from rag.store import NumpyVectorstore  # noqa: E402

# Le ultime quattro domande del probe sono deliberatamente fuori corpus.
OUT_OF_CORPUS = {
    "Qual è il fatturato annuo di Booster Robotics?",
    "Quante persone hanno assistito al match dal vivo?",
    "Che sponsor tecnico ha pagato le divise della squadra umana?",
    "Qual è il regolamento FIFA applicato al match?",
}


def main() -> int:
    index_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "index"
    store = NumpyVectorstore.load(index_dir)
    probe = json.loads((index_dir / "probe-queries.json").read_text(encoding="utf-8"))
    retriever = HybridRetriever(store, embedder=None)  # embedder non serve

    matrix = store._matrix["prometeo"]
    norms = np.linalg.norm(matrix, axis=1)

    rows = []
    for item in probe["queries"]:
        q, vec = item["text"], item["vector"]
        hits = retriever.search(q, k=10, query_vector=vec)
        v = np.asarray(vec, dtype=np.float32)
        cos = float(((matrix @ v) / (norms * np.linalg.norm(v) + 1e-10)).max())
        margin = (hits[0].score - hits[-1].score) / hits[0].score if len(hits) >= 10 else 0.0
        fuori = q in OUT_OF_CORPUS
        rows.append((q, hits, cos, margin, fuori))

        print("=" * 100)
        print(("[FUORI CORPUS] " if fuori else "") + q)
        print(f"   coseno max {cos:.3f} · margine testa-coda {margin:.1%}")
        for h in hits[:3]:
            m = h.chunk.metadata
            print(f"     {h.score:.4f} {h.why:26} {m['register']:12} {m['citation'][:66]}")
            print(f"            {h.chunk.text[:118].replace(chr(10), ' / ')}")

    print("\n" + "=" * 100)
    dentro = [r for r in rows if not r[4]]
    fuori = [r for r in rows if r[4]]
    for nome, gruppo in (("dentro corpus", dentro), ("fuori corpus", fuori)):
        if not gruppo:
            continue
        c = [r[2] for r in gruppo]
        print(f"{nome:16} n={len(gruppo):2}  coseno max: media {np.mean(c):.3f} "
              f"min {min(c):.3f} max {max(c):.3f}")
    if dentro and fuori:
        soglia = (min(r[2] for r in dentro) + max(r[2] for r in fuori)) / 2
        separabile = min(r[2] for r in dentro) > max(r[2] for r in fuori)
        print(f"\nsoglia candidata: {soglia:.3f} — separazione netta: "
              f"{'SI' if separabile else 'NO, le due nuvole si sovrappongono'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
