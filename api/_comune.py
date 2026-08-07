"""
Parti condivise dalle due funzioni serverless.

Il caricamento dell'indice avviene una volta per istanza calda: 224 vettori da
1024 float sono 900 KB, si leggono in millisecondi e restano in memoria fra una
richiesta e l'altra.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RADICE / "services" / "api"))

INDICE = RADICE / "index"

_stato: dict = {}


def carica():
    """Store, retriever ed embedder, una volta sola per istanza."""
    if _stato:
        return _stato
    from rag.retrieve import HybridRetriever
    from rag.store import NumpyVectorstore

    info = json.loads((INDICE / "build-info.json").read_text(encoding="utf-8"))
    # In locale si puo' girare senza chiavi di embedding usando il ripiego
    # TF-IDF: serve a collaudare la catena degli endpoint prima di avere il
    # fornitore. In produzione EMBEDDING_PROVIDER vale voyage o openai.
    if os.environ.get("EMBEDDING_PROVIDER", "").lower() == "tfidf":
        from rag.embedder_offline import TfidfEmbedder
        embedder = TfidfEmbedder.load(INDICE)
    else:
        from rag.embedder_api import ApiEmbedder
        embedder = ApiEmbedder()

    # Il controllo che evita il guasto piu' insidioso: un indice costruito con
    # un modello e interrogato con un altro non da' errore, da' risultati
    # plausibili e sbagliati. Meglio rifiutarsi di partire.
    atteso = info.get("model")
    if atteso and atteso != embedder.model_name:
        raise RuntimeError(
            f"indice costruito con {atteso}, embedder configurato su "
            f"{embedder.model_name}: ricostruire l'indice prima di servire")

    store = NumpyVectorstore.load(INDICE)
    _stato.update(store=store, embedder=embedder, info=info,
                  retriever=HybridRetriever(store, embedder))
    return _stato


def risposta(handler, corpo: dict, stato: int = 200):
    dati = json.dumps(corpo, ensure_ascii=False).encode()
    handler.send_response(stato)
    handler.send_header("content-type", "application/json; charset=utf-8")
    handler.send_header("content-length", str(len(dati)))
    handler.end_headers()
    handler.wfile.write(dati)


def leggi(handler) -> dict:
    n = int(handler.headers.get("content-length") or 0)
    return json.loads(handler.rfile.read(n) or b"{}")
