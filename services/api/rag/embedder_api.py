"""
Embedder via API, per far girare la catena dove e5 non ci sta.

e5-large pesa 2,2 GB. Sta dentro le large functions di Vercel (fino a 5 GB) ma
vorrebbe fluid compute, memoria da piano Pro, e ogni avvio a freddo caricherebbe
il modello: decine di secondi per il primo che apre la pagina. Per una demo che
qualcuno apre una volta e' il compromesso sbagliato.

Con l'embedding via API la funzione ha bisogno solo di httpx e numpy: pochi
megabyte, avvio istantaneo. Il resto della catena non cambia di una riga, ed e'
esattamente il motivo per cui `BaseEmbedder` esisteva gia'.

ATTENZIONE, la regola che fa fallire tutto se la si dimentica: cambiare
embedder significa cambiare spazio vettoriale. L'indice va RICOSTRUITO con lo
stesso modello, altrimenti le distanze non vogliono dire niente e il retrieval
restituisce risultati plausibili e casuali. `build_index.py` scrive il modello
usato in build-info.json apposta: al caricamento si controlla che coincida.
"""

from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request

from datapizza.core.embedder import BaseEmbedder
from datapizza.type import DenseEmbedding

# Due fornitori, stessa forma di richiesta. Voyage e' il partner consigliato da
# Anthropic; OpenAI e' quello che quasi tutti hanno gia'. Il codice non prende
# posizione: legge EMBEDDING_PROVIDER.
def _contesto_ssl() -> ssl.SSLContext | None:
    """Certificati espliciti invece di quelli di sistema.

    Il Python di python.org su macOS porta il proprio OpenSSL e non legge il
    portachiavi: senza aver lanciato "Install Certificates.command" ogni
    chiamata HTTPS fatta con urllib muore con CERTIFICATE_VERIFY_FAILED. Le
    chiamate ad Anthropic non se ne accorgono perche' il loro SDK usa httpx,
    che si porta certifi dentro. Qui facciamo lo stesso, cosi' lo script non
    dipende da un passaggio manuale che nessuno ricorda di aver saltato.
    """
    try:
        import certifi
    except ImportError:
        return None
    return ssl.create_default_context(cafile=certifi.where())


_SSL = _contesto_ssl()

# I piani gratuiti dei fornitori di embedding hanno limiti di frequenza
# stretti. Mandare 224 chunk in due blocchi da 128 li supera, e il 429 arriva
# a meta' indicizzazione lasciando l'indice a meta'. Blocchi piccoli, una
# pausa fra l'uno e l'altro, e ritentativi con attesa crescente.
BLOCCO = int(os.environ.get("EMBEDDING_BATCH", "32"))
PAUSA = float(os.environ.get("EMBEDDING_PAUSA", "1.0"))
RITENTATIVI = 6


def _con_ritenta(fn, *args, **kwargs):
    """Riprova sui 429 e sui guasti temporanei, rispettando Retry-After.

    Un 429 non e' un errore del programma: e' il fornitore che dice "piu'
    piano". Trattarlo come fatale significa far rilanciare tutto all'utente,
    che e' esattamente quello che un programma dovrebbe evitargli.
    """
    attesa = 2.0
    for tentativo in range(1, RITENTATIVI + 1):
        try:
            return fn(*args, **kwargs)
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 529) or tentativo == RITENTATIVI:
                raise
            suggerita = e.headers.get("retry-after") if e.headers else None
            pausa = float(suggerita) if (suggerita or "").replace(".", "").isdigit() else attesa
            print(f"    {e.code}: attendo {pausa:.0f}s e riprovo "
                  f"({tentativo}/{RITENTATIVI - 1})", flush=True)
            time.sleep(pausa)
            attesa = min(attesa * 2, 60)

FORNITORI = {
    "voyage": {
        "url": "https://api.voyageai.com/v1/embeddings",
        "modello": "voyage-3",
        "chiave_env": "VOYAGE_API_KEY",
        "dimensioni": 1024,
    },
    "openai": {
        "url": "https://api.openai.com/v1/embeddings",
        "modello": "text-embedding-3-small",
        "chiave_env": "OPENAI_API_KEY",
        "dimensioni": 1536,
    },
}


class ApiEmbedder(BaseEmbedder):
    """Embedding remoto. Nessun modello da scaricare, nessun peso da caricare."""

    def __init__(self, fornitore: str | None = None, modello: str | None = None,
                 embedding_name: str = "dense"):
        nome = (fornitore or os.environ.get("EMBEDDING_PROVIDER", "voyage")).lower()
        if nome not in FORNITORI:
            raise ValueError(f"fornitore sconosciuto: {nome} (attesi: {list(FORNITORI)})")
        self.fornitore = nome
        self.conf = FORNITORI[nome]
        self.model_name = modello or self.conf["modello"]
        self.embedding_name = embedding_name

    @property
    def dimensioni_attese(self) -> int:
        return int(self.conf["dimensioni"])

    @property
    def dimensions(self) -> int:
        return self.dimensioni_attese

    def _chiave(self) -> str:
        chiave = os.environ.get(self.conf["chiave_env"], "")
        if not chiave:
            raise RuntimeError(
                f"{self.conf['chiave_env']} assente: serve per l'embedding via API")
        return chiave

    def _chiama(self, testi: list[str], tipo: str = "document") -> list[list[float]]:
        corpo = {"model": self.model_name, "input": testi}
        if self.fornitore == "voyage":
            # voyage distingue documenti e domande: usarlo migliora il retrieval
            corpo["input_type"] = tipo
        req = urllib.request.Request(
            self.conf["url"], data=json.dumps(corpo).encode(),
            headers={"content-type": "application/json",
                     "authorization": f"Bearer {self._chiave()}"})
        with urllib.request.urlopen(req, timeout=60, context=_SSL) as r:
            dati = json.load(r)
        # entrambi i fornitori restituiscono data[] ordinato per index
        righe = sorted(dati["data"], key=lambda x: x.get("index", 0))
        return [r["embedding"] for r in righe]

    # ---- interfaccia datapizza -------------------------------------------

    def _a_blocchi(self, testi: list[str], tipo: str) -> list[list[float]]:
        """Il solo posto da cui esce una richiesta di embedding.

        Una richiesta per blocco, mai una per testo: i limiti di frequenza dei
        fornitori contano le richieste, non i caratteri. Venticinque domande
        mandate una alla volta diventano venticinque 429 con attesa crescente —
        mezz'ora — mentre le stesse venticinque in un blocco solo sono una
        richiesta e qualche secondo.
        """
        vettori: list[list[float]] = []
        blocchi = [testi[i:i + BLOCCO] for i in range(0, len(testi), BLOCCO)]
        for n, blocco in enumerate(blocchi, 1):
            if len(blocchi) > 1:
                print(f"  blocco {n}/{len(blocchi)} ({len(blocco)} testi)", flush=True)
            vettori.extend(_con_ritenta(self._chiama, blocco, tipo))
            if n < len(blocchi):
                time.sleep(PAUSA)
        return vettori

    def embed(self, text: str | list[str], **kwargs):
        singolo = isinstance(text, str)
        testi = [text] if singolo else list(text)
        if not testi:
            return []
        vettori = self._a_blocchi(testi, "document")
        return vettori[0] if singolo else vettori

    async def a_embed(self, text: str | list[str], **kwargs):
        return self.embed(text, **kwargs)

    # ---- comodita' --------------------------------------------------------

    def embed_query(self, text: str) -> list[float]:
        return self._a_blocchi([text], "query")[0]

    def embed_queries(self, testi: list[str]) -> list[list[float]]:
        """Piu' domande in una richiesta sola. Da preferire sempre al ciclo."""
        return self._a_blocchi(list(testi), "query") if testi else []

    def embed_passages(self, texts: list[str]) -> list[list[float]]:
        return self.embed(texts)

    def as_dense(self, vector: list[float]) -> DenseEmbedding:
        return DenseEmbedding(name=self.embedding_name, vector=vector)
