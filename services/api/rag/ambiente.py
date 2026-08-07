"""
Le variabili di .env dentro os.environ, una volta sola e senza stamparle.

Serve a togliere di mezzo un errore che si ripresenta ogni volta: gli script
leggono le chiavi da os.environ, ma .env e' un file, non un ambiente. Chi
dimentica di fare `source .env` non ottiene un messaggio chiaro — ottiene un
"VOYAGE_API_KEY assente" a meta' di una build da quattro minuti, oppure, peggio,
un ripiego silenzioso su un altro embedder che manda l'indice in un altro spazio
vettoriale.

Due regole, entrambe deliberate:

  - l'ambiente vero vince sempre sul file. Su Vercel le variabili arrivano dalla
    console e .env non esiste nemmeno; in locale, chi esporta una chiave a mano
    per una prova si aspetta che sia quella a valere.
  - i valori non si stampano e non si restituiscono. La funzione dice quali nomi
    ha caricato, mai cosa contengono, cosi' non finiscono in un log per
    disattenzione.
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def carica_env(percorso: Path | None = None) -> list[str]:
    """Carica .env in os.environ. Restituisce i NOMI caricati, mai i valori."""
    env = percorso or ROOT / ".env"
    if not env.exists():
        return []
    caricati: list[str] = []
    for riga in env.read_text(encoding="utf-8").splitlines():
        riga = riga.strip()
        if not riga or riga.startswith("#") or "=" not in riga:
            continue
        nome, valore = riga.split("=", 1)
        nome = nome.strip()
        if not nome or os.environ.get(nome):
            continue
        os.environ[nome] = valore.strip().strip('"').strip("'")
        caricati.append(nome)
    return caricati
