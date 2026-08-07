"""
GET /api/diag  ->  cosa vede davvero la funzione, senza spendere un centesimo.

Nasce da un'ora persa su un FUNCTION_INVOCATION_FAILED: cinquecento senza corpo,
senza traccia, senza niente. Un errore che non si legge costa piu' di quello che
nasconde, e le due funzioni vere non possono raccontarlo perche' se crollano
crollano prima di poter parlare.

Questa non importa nulla di pesante al primo livello e prova un pezzo per volta,
dicendo quale regge e quale no. Sui segreti riporta solo se ci sono: mai un
valore, nemmeno troncato.
"""

import json
import os
import sys
import traceback
from http.server import BaseHTTPRequestHandler
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]

MODULI = ["rag.store", "rag.retrieve", "rag.embedder_api", "rag.budget",
          "rag.llm", "rag.verify"]

ATTESI = ["index/build-info.json", "index/prometeo.chunks.json",
          "index/prometeo.vectors.npy", "services/api/rag/retrieve.py"]


def _prova(fn):
    """Esegue e restituisce l'esito come stringa, senza mai sollevare."""
    try:
        return {"ok": True, "valore": fn()}
    except BaseException as e:
        return {"ok": False, "errore": f"{type(e).__name__}: {e}",
                "traccia": traceback.format_exc().splitlines()[-6:]}


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        esito = {
            "python": sys.version.split()[0],
            "radice": str(RADICE),
            "cwd": os.getcwd(),
            "file_attesi": {p: (RADICE / p).exists() for p in ATTESI},
            "contenuto_radice": sorted(x.name for x in RADICE.iterdir())[:40],
            # dei segreti diciamo solo se ci sono. Mai quanto sono lunghi,
            # mai un prefisso: un prefisso e' gia' un'informazione di troppo.
            "variabili": {n: bool(os.environ.get(n)) for n in
                          ("ANTHROPIC_API_KEY", "VOYAGE_API_KEY",
                           "OPENAI_API_KEY", "EMBEDDING_PROVIDER",
                           "BUDGET_MAX_USD")},
            "embedding_provider": os.environ.get("EMBEDDING_PROVIDER") or "(non impostata)",
        }

        sys.path.insert(0, str(RADICE / "services" / "api"))
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        esito["moduli"] = {}
        for nome in MODULI:
            esito["moduli"][nome] = _prova(
                lambda n=nome: __import__(n) and "importato")

        def _carica():
            from _comune import carica
            s = carica()
            return {"modello": s["info"].get("model"),
                    "chunk": s["info"].get("chunks")}
        esito["carica"] = _prova(_carica)

        dati = json.dumps(esito, ensure_ascii=False, indent=2).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json; charset=utf-8")
        self.send_header("content-length", str(len(dati)))
        self.end_headers()
        self.wfile.write(dati)
