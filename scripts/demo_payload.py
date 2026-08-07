#!/usr/bin/env python3
"""
Produce il JSON che alimenta la demo: risposte vere, verdetti veri, prove vere.

    python3 scripts/demo_payload.py [cartella_indice]

Niente e' scritto a mano. Ogni riga del pannello fonti nasce da una chiamata
davvero eseguita, e gli estratti sono letti dal file sorgente agli offset
calcolati dal chunker. Se un giorno il corpus cambia e una prova sparisce, la
demo lo mostra invece di continuare a raccontare la vecchia storia.

Scrive apps/web/demo-data.json.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services" / "api"))

from rag.retrieve import HybridRetriever  # noqa: E402
from rag.store import NumpyVectorstore  # noqa: E402
from rag.verify import verifica_risposta  # noqa: E402

sys.path.insert(0, str(ROOT / "scripts"))
from slice import rispondi  # noqa: E402

CORPUS = ROOT / "corpus" / "prometeo-cup" / "channels"

# Tre domande scelte per far vedere i quattro stati e le due annotazioni:
# una risposta pulita, una che inciampa in una contraddizione dell'archivio,
# una che aggrega numeri che cambiano nel tempo, una su cui l'archivio tace.
DOMANDE = [0, 20, 17, 21]


def estratto(source_file: str, start: int, end: int, margine: int = 260) -> dict:
    """Il testo attorno alla prova, letto dal file sorgente."""
    p = CORPUS / source_file
    if not p.exists():
        return {}
    testo = p.read_text(encoding="utf-8")
    a, b = max(0, start - margine), min(len(testo), end + margine)
    # taglia su confini di riga: un contesto che parte a meta' parola
    # sembra un errore di rendering e distrae da cio' che conta
    if a > 0:
        nl = testo.find("\n", a, start)
        a = nl + 1 if nl != -1 else a
    nl = testo.rfind("\n", end, b)
    b = nl if nl != -1 else b
    return {"prima": testo[a:start], "prova": testo[start:end], "dopo": testo[end:b]}


def main() -> int:
    index_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "index"
    store = NumpyVectorstore.load(index_dir)
    probe = json.loads((index_dir / "probe-queries.json").read_text(encoding="utf-8"))
    retriever = HybridRetriever(store, embedder=None)

    fuori = []
    for idx in DOMANDE:
        item = probe["queries"][idx]
        domanda, vec = item["text"], item["vector"]
        hits = retriever.search(domanda, k=8, query_vector=vec)
        print(f"· {domanda}")
        risposta = rispondi(domanda, hits)
        affermazioni = []
        for a in verifica_risposta(risposta, hits):
            riga = {
                "testo": a.testo,
                "stato": a.stato,
                "colore": a.colore,
                "confidenza": round(a.confidenza, 2),
                "motivo": a.motivo,
                "passaggi": a.passaggi,
                "ancora_scartata": a.ancora_scartata,
                "citazione_fantasma": a.citazione_fantasma,
            }
            if a.ancora:
                riga["ancora"] = {
                    "citazione": a.ancora.citazione,
                    "dove": a.ancora.citation_label,
                    "file": a.ancora.source_file,
                    "inizio": a.ancora.inizio_nel_file,
                    "fine": a.ancora.fine_nel_file,
                    "contesto": estratto(a.ancora.source_file,
                                         a.ancora.inizio_nel_file,
                                         a.ancora.fine_nel_file),
                }
            if a.conflitto:
                c = a.conflitto
                riga["conflitto"] = {"nota": c.nota, "prima": c.prima, "dopo": c.dopo}
            affermazioni.append(riga)
            print(f"    {a.colore:10} {a.testo[:70]}")

        fuori.append({
            "domanda": domanda,
            "risposta": risposta,
            "affermazioni": affermazioni,
            "passaggi_recuperati": [
                {"citazione": (h.chunk.metadata or {}).get("citation", ""),
                 "quando": (h.chunk.metadata or {}).get("timestamp"),
                 "registro": (h.chunk.metadata or {}).get("register", ""),
                 "come": h.why,
                 "testo": h.chunk.text}
                for h in hits
            ],
        })

    info = json.loads((index_dir / "build-info.json").read_text(encoding="utf-8"))
    out = ROOT / "apps" / "web" / "demo-data.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"indice": info, "casi": fuori},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nscritto {out} ({out.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
