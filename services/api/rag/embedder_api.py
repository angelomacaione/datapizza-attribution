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
import urllib.request

from datapizza.core.embedder import BaseEmbedder
from datapizza.type import DenseEmbedding

# Due fornitori, stessa forma di richiesta. Voyage e' il partner consigliato da
# Anthropic; OpenAI e' quello che quasi tutti hanno gia'. Il codice non prende
# posizione: legge EMBEDDING_PROVIDER.
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

    def _chiama(self, testi: list[str]) -> list[list[float]]:
        corpo = {"model": self.model_name, "input": testi}
        if self.fornitore == "voyage":
            # voyage distingue documenti e domande: usarlo migliora il retrieval
            corpo["input_type"] = "document"
        req = urllib.request.Request(
            self.conf["url"], data=json.dumps(corpo).encode(),
            headers={"content-type": "application/json",
                     "authorization": f"Bearer {self._chiave()}"})
        with urllib.request.urlopen(req, timeout=60) as r:
            dati = json.load(r)
        # entrambi i fornitori restituiscono data[] ordinato per index
        righe = sorted(dati["data"], key=lambda x: x.get("index", 0))
        return [r["embedding"] for r in righe]

    # ---- interfaccia datapizza -------------------------------------------

    def embed(self, text: str | list[str], **kwargs):
        singolo = isinstance(text, str)
        testi = [text] if singolo else list(text)
        if not testi:
            return [] if not singolo else []
        vettori = []
        # i fornitori hanno tetti sul numero di input per chiamata: 128 e' un
        # valore prudente per entrambi
        for i in range(0, len(testi), 128):
            vettori.extend(self._chiama(testi[i:i + 128]))
        return vettori[0] if singolo else vettori

    async def a_embed(self, text: str | list[str], **kwargs):
        return self.embed(text, **kwargs)

    # ---- comodita' --------------------------------------------------------

    def embed_query(self, text: str) -> list[float]:
        if self.fornitore == "voyage":
            corpo_query = self._chiama_query(text)
            return corpo_query
        return self.embed(text)

    def _chiama_query(self, testo: str) -> list[float]:
        corpo = {"model": self.model_name, "input": [testo], "input_type": "query"}
        req = urllib.request.Request(
            self.conf["url"], data=json.dumps(corpo).encode(),
            headers={"content-type": "application/json",
                     "authorization": f"Bearer {self._chiave()}"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)["data"][0]["embedding"]

    def embed_passages(self, texts: list[str]) -> list[list[float]]:
        return self.embed(texts)

    def as_dense(self, vector: list[float]) -> DenseEmbedding:
        return DenseEmbedding(name=self.embedding_name, vector=vector)
