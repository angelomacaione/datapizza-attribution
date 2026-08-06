#!/usr/bin/env python3
"""
La fetta verticale: domanda -> recupero -> risposta -> giudizio -> quattro stati.

    python3 scripts/slice.py [cartella_indice] [numero_domanda ...]

Senza argomenti gira su tre domande scelte apposta: una a cui l'archivio
risponde per intero, una che richiede di comporre piu' canali, e una di cui
l'archivio non parla affatto.

Usa i vettori precalcolati in probe-queries.json, cosi' gira anche dove il
modello di embedding non e' scaricabile.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services" / "api"))

from rag.llm import estensore  # noqa: E402
from rag.retrieve import HybridRetriever  # noqa: E402
from rag.store import NumpyVectorstore  # noqa: E402
from rag.verify import verifica_risposta  # noqa: E402

SIMBOLO = {"ripescato": "● verde    ", "inferito": "● blu      ",
           "non_supportato": "● rosso    ", "fuori_corpus": "● arancione"}

DEFAULT = [0, 6, 16]   # rental K1 · e-stop livello 3 · fatturato Booster (fuori corpus)


def rispondi(domanda: str, hits) -> str:
    # Le date vanno date anche all'estensore, non solo al giudice: nasconderle
    # renderebbe le trappole temporali piu' vistose ma sarebbe una partita
    # truccata. Se sbaglia avendole viste, il fallimento e' reale.
    passaggi = "\n\n".join(
        f"[{i}] {(h.chunk.metadata or {}).get('timestamp') or 'data ignota'} — "
        f"({(h.chunk.metadata or {}).get('citation','')})\n{h.chunk.text}"
        for i, h in enumerate(hits, 1))
    prompt = (f"PASSAGGI DALL'ARCHIVIO:\n\n{passaggi}\n\n"
              f"DOMANDA:\n{domanda}")
    return estensore().invoke(input=prompt).text.strip()


def main() -> int:
    args = sys.argv[1:]
    index_dir = Path(args[0]) if args and not args[0].isdigit() else ROOT / "index"
    scelte = [int(a) for a in args if a.isdigit()] or DEFAULT

    store = NumpyVectorstore.load(index_dir)
    probe = json.loads((index_dir / "probe-queries.json").read_text(encoding="utf-8"))
    retriever = HybridRetriever(store, embedder=None)

    for idx in scelte:
        item = probe["queries"][idx]
        domanda, vec = item["text"], item["vector"]
        hits = retriever.search(domanda, k=8, query_vector=vec)

        print("=" * 100)
        print(f"DOMANDA  {domanda}")
        print("-" * 100)
        risposta = rispondi(domanda, hits)
        print(risposta)
        print("-" * 100)

        for a in verifica_risposta(risposta, hits):
            print(f"{SIMBOLO[a.stato]} conf {a.confidenza:.2f}  {a.testo[:92]}")
            print(f"              perche': {a.motivo[:88]}")
            if a.ancora:
                print(f"              verbatim: \"{a.ancora.citazione[:76]}\"")
                print(f"              in {a.ancora.source_file} "
                      f"[{a.ancora.inizio_nel_file}:{a.ancora.fine_nel_file}] "
                      f"— {a.ancora.citation_label[:56]}")
            if a.ancora_scartata:
                print(f"              ✂ prova scartata dal revisore: {a.ancora_scartata[:110]}")
            if a.citazione_fantasma:
                print(f"              ⚠ il giudice ha citato un frammento che NON esiste: "
                      f"\"{a.citazione_fantasma[:62]}\"")
            if a.conflitto:
                c=a.conflitto
                print(f"              ⏳ CONFLITTO TEMPORALE — {c.nota[:78]}")
                print(f"                 {c.prima['quando']}  {c.prima['dove'][:66]}")
                print(f"                 {c.dopo['quando']}  {c.dopo['dove'][:66]}")
            if not a.ancora and a.passaggi:
                etichette = ", ".join(p["citation"][:44] for p in a.passaggi[:2])
                print(f"              cucito da: {etichette}")
            print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
