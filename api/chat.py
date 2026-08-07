"""
POST /api/chat  ->  { domanda }  ->  { risposta, passaggi, hits_id }

Risponde e basta. La verifica sta in /api/verify, chiamata dal browser una
frase alla volta: cosi' nessuna richiesta si avvicina al limite di durata, e
soprattutto l'utente vede la risposta subito e i verdetti arrivare dopo,
invece di fissare uno spinner per quaranta secondi.
"""

import sys
from pathlib import Path

# Vercel non esegue la funzione dalla cartella api/: il suo involucro sta in
# /var/task e da li' parte tutto, quindi la cartella di QUESTO file non e' in
# sys.path e `import _comune` muore con ModuleNotFoundError. Muore al primo
# livello del modulo — prima che qualsiasi try possa intercettarlo — e la
# funzione crolla muta: FUNCTION_INVOCATION_FAILED, cinquecento senza corpo.
# In locale non si vedeva perche' gli script partivano da dentro api/.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from http.server import BaseHTTPRequestHandler

from _comune import carica, leggi, risposta

# Gli import pesanti si fanno all'avvio dell'istanza, non dentro il try di
# do_POST. Farli li' dentro ha un difetto che si paga caro: se l'import
# fallisce, BudgetEsaurito non viene mai definito, e Python va a valutare
# `except BudgetEsaurito` trovando un nome non assegnato. L'eccezione della
# clausola except sostituisce quella vera e la funzione muore muta —
# FUNCTION_INVOCATION_FAILED, cinquecento senza corpo, nessuna traccia.
# Qui l'errore d'avvio viene conservato e restituito come JSON leggibile.
AVVIO = None
try:
    from rag.budget import BudgetEsaurito, protetta
    from rag.llm import estensore
except BaseException as _e:  # noqa: BLE001 - qualunque cosa, purche' si legga
    import traceback as _tb
    AVVIO = {"errore": f"{type(_e).__name__}: {_e}",
             "traccia": _tb.format_exc().splitlines()[-8:]}

    class BudgetEsaurito(Exception):
        motivo = "modulo non caricato"



class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if AVVIO:
            return risposta(self, {"errore": "avvio della funzione fallito",
                                   **AVVIO}, 500)
        try:
            corpo = leggi(self)
            domanda = (corpo.get("domanda") or "").strip()
            if not domanda:
                return risposta(self, {"errore": "domanda vuota"}, 400)
            if len(domanda) > 500:
                return risposta(self, {"errore": "domanda troppo lunga"}, 400)

            stato = carica()
            hits = stato["retriever"].search(domanda, k=8)
            passaggi = "\n\n".join(
                f"[{i}] {(h.chunk.metadata or {}).get('timestamp') or 'data ignota'} — "
                f"({(h.chunk.metadata or {}).get('citation','')})\n{h.chunk.text}"
                for i, h in enumerate(hits, 1))

            r = protetta(estensore().invoke,
                         input=f"PASSAGGI DALL'ARCHIVIO:\n\n{passaggi}\n\nDOMANDA:\n{domanda}")
            return risposta(self, {
                "domanda": domanda,
                "risposta": r.text.strip(),
                "chunk_ids": [h.chunk.id for h in hits],
                "passaggi_recuperati": [
                    {"citazione": (h.chunk.metadata or {}).get("citation", ""),
                     "quando": (h.chunk.metadata or {}).get("timestamp"),
                     "come": h.why}
                    for h in hits],
            })
        except BudgetEsaurito as e:
            return risposta(self, {"esaurito": True, "motivo": e.motivo}, 402)
        except Exception as e:
            return risposta(self, {"errore": f"{type(e).__name__}: {e}"}, 500)
