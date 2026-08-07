#!/usr/bin/env python3
"""
Vettorializza una lista di domande di prova e le scrive in un JSON.

Serve a un caso preciso: l'ambiente in cui sviluppo non raggiunge HuggingFace,
quindi non posso caricare e5 e non posso vettorializzare una domanda. I vettori
dei chunk viaggiano bene (sono un file), le domande no. Con questo script le
domande vengono vettorializzate qui, dove il modello c'e', e il risultato
diventa un file trasportabile come gli altri.

    source .venv/bin/activate
    python scripts/embed_queries.py

Scrive index/probe-queries.json (~40 KB). Dura pochi secondi: il modello e'
gia' in cache dopo la build.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services" / "api"))

from rag.ambiente import carica_env  # noqa: E402

carica_env()   # .env -> os.environ, cosi' non serve ricordarsi di sourcearlo

from rag.embedder import LocalEmbedder  # noqa: E402


def scegli_embedder():
    """Lo stesso modello dell'indice, o i vettori non vogliono dire niente.

    Le domande e i chunk devono vivere nello stesso spazio vettoriale. e5 e
    voyage-3 hanno per caso la stessa dimensione (1024): mescolarli non da'
    errore, da' un recupero plausibile e sbagliato. Quindi qui si legge la
    stessa variabile che comanda la build.
    """
    fornitore = os.environ.get("EMBEDDING_PROVIDER", "").lower()
    if fornitore in ("voyage", "openai"):
        from rag.embedder_api import ApiEmbedder
        return ApiEmbedder(fornitore)
    return LocalEmbedder()

# Domande scelte per coprire i modi diversi in cui il retrieval puo' rompersi:
# cifre esatte, codici prodotto, attribuzione di responsabilita', fatti sparsi
# su piu' canali, e cose di cui il vault NON parla (che devono NON trovare
# nulla di buono: e' il caso "fuori corpus").
QUERIES = [
    # cifre e importi
    "Quanto costa il noleggio del K1 demo da Génération Robots?",
    "Di quanto è sceso il contingency dopo il delta budget dell'illuminazione?",
    "Quanto è costato il trasporto dei NAO da Sapienza?",
    # codici e hardware
    "Cosa è successo a K1-03 durante il dry run DR2?",
    "Perché K1-08 è arrivato in ritardo?",
    "Quanti robot erano previsti in campo per DR2?",
    # attribuzione e responsabilita'
    "Chi ha in mano il trigger dell'e-stop di livello 3?",
    "Chi ha deciso il rental del K1 da Génération Robots?",
    "Chi è il Safety Officer in campo il giorno dell'evento?",
    # fatti medici e sensibili
    "Marco Fusco può giocare il primo tempo?",
    "Cosa è successo a Silvia l'8 novembre?",
    # decisioni di processo
    "Perché DR3 non è stato fatto?",
    "Quando è stato fissato il freeze del codice SPQR?",
    "Che problema ha dato l'illuminazione del padiglione?",
    # cose sparse su piu' canali, dove il registro cambia
    "Come è stata gestita la comunicazione con la stampa e l'embargo?",
    "Qual era lo stato d'animo della squadra la notte prima dell'evento?",
    # trappole temporali: ricavate da conflitti reali trovati nel corpus da
    # find_contradictions.py. Ognuna ha due risposte vere in momenti diversi,
    # e quella sbagliata e' la piu' facile da pescare.
    "Qual e' il tag della versione finale del codice utilizzata per DR2?",
    "Quanti dottorandi SPQR hanno partecipato alle riunioni tecniche?",
    "Il crisis statement per l'infortunio di un dipendente e' gia' stato approvato?",
    "Come si comporta il portiere robotico durante la partita?",
    "Chi ha in mano il trigger dell'e-stop il giorno dell'evento?",
    # fuori corpus: il vault non ne parla, il sistema deve dirlo
    "Qual è il fatturato annuo di Booster Robotics?",
    "Quante persone hanno assistito al match dal vivo?",
    "Che sponsor tecnico ha pagato le divise della squadra umana?",
    "Qual è il regolamento FIFA applicato al match?",
]


def main() -> int:
    embedder = scegli_embedder()
    print(f"modello: {embedder.model_name} (dim {embedder.dimensions})")
    vectors = [embedder.embed_query(q) for q in QUERIES]
    out = ROOT / "index" / "probe-queries.json"
    out.write_text(json.dumps({
        "model": embedder.model_name,
        "dimensions": embedder.dimensions,
        "queries": [{"text": q, "vector": v} for q, v in zip(QUERIES, vectors)],
    }, ensure_ascii=False), encoding="utf-8")
    size = out.stat().st_size / 1024
    print(f"scritte {len(QUERIES)} domande in {out} ({size:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
