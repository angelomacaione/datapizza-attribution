"""
POST /api/chat  ->  { domanda }  ->  { risposta, passaggi, hits_id }

Risponde e basta. La verifica sta in /api/verify, chiamata dal browser una
frase alla volta: cosi' nessuna richiesta si avvicina al limite di durata, e
soprattutto l'utente vede la risposta subito e i verdetti arrivare dopo,
invece di fissare uno spinner per quaranta secondi.
"""

from http.server import BaseHTTPRequestHandler

from _comune import carica, leggi, risposta


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            corpo = leggi(self)
            domanda = (corpo.get("domanda") or "").strip()
            if not domanda:
                return risposta(self, {"errore": "domanda vuota"}, 400)
            if len(domanda) > 500:
                return risposta(self, {"errore": "domanda troppo lunga"}, 400)

            from rag.budget import BudgetEsaurito, protetta
            from rag.llm import estensore

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
