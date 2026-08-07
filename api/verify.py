"""
POST /api/verify  ->  { frase, chunk_ids }  ->  un verdetto

Una frase per richiesta. Il browser le lancia in parallelo e accende le frasi
man mano che i verdetti tornano: si vede la verifica accadere, che e' la cosa
che questa demo deve mostrare.
"""

from http.server import BaseHTTPRequestHandler

from _comune import carica, leggi, risposta


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            corpo = leggi(self)
            frase = (corpo.get("frase") or "").strip()
            ids = corpo.get("chunk_ids") or []
            if not frase or not ids:
                return risposta(self, {"errore": "frase o chunk_ids mancanti"}, 400)

            from rag.budget import BudgetEsaurito
            from rag.retrieve import Hit
            from rag.verify import verifica_affermazione

            stato = carica()
            per_id = {c.id: c for c in stato["store"].all_chunks()}
            hits = [Hit(chunk=per_id[i], score=1.0, dense_rank=None,
                        lexical_rank=None, why="ripreso da /api/chat")
                    for i in ids if i in per_id]
            if not hits:
                return risposta(self, {"errore": "nessun passaggio valido"}, 400)

            a = verifica_affermazione(frase, hits)
            fuori = {"testo": a.testo, "stato": a.stato, "colore": a.colore,
                     "confidenza": round(a.confidenza, 2), "motivo": a.motivo,
                     "passaggi": a.passaggi,
                     "ancora_scartata": a.ancora_scartata,
                     "citazione_fantasma": a.citazione_fantasma}
            if a.ancora:
                fuori["ancora"] = {"citazione": a.ancora.citazione,
                                   "dove": a.ancora.citation_label,
                                   "file": a.ancora.source_file,
                                   "inizio": a.ancora.inizio_nel_file,
                                   "fine": a.ancora.fine_nel_file}
            if a.conflitto:
                fuori["conflitto"] = {"nota": a.conflitto.nota,
                                      "prima": a.conflitto.prima,
                                      "dopo": a.conflitto.dopo}
            return risposta(self, fuori)
        except BudgetEsaurito as e:
            return risposta(self, {"esaurito": True, "motivo": e.motivo}, 402)
        except Exception as e:
            return risposta(self, {"errore": f"{type(e).__name__}: {e}"}, 500)
