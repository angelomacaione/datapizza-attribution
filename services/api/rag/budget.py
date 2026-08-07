"""
Il freno di spesa, e la discesa morbida quando scatta.

Perche' sta qui e non solo in console. La documentazione di Anthropic descrive
i limiti di workspace come *spend notifications* e non dichiara da nessuna parte
che le richieste vengano bloccate al raggiungimento del tetto, ne' con quale
errore. Costruire il comportamento della demo su una semantica non documentata
significherebbe scoprirla il giorno del colloquio.

Quindi: la console tiene i soldi (credito prepagato + rate limit del workspace),
questo modulo tiene l'esperienza. Reagisce a cio' che l'API risponde davvero, e
in piu' si auto-limita prima ancora di chiamare.

Due freni, in ordine di intervento:

  1. tetto locale — stimiamo la spesa a ogni chiamata e ci fermiamo prima di
     superare il budget. Non richiede stato condiviso: in serverless ogni
     istanza tiene il proprio conto, quindi e' una stima prudente per istanza,
     non un totale esatto. Serve a non arrivare mai al muro.
  2. errore dell'API — se il muro lo tocchiamo lo stesso (credito esaurito,
     rate limit), lo riconosciamo e degradiamo invece di mostrare un errore.

In entrambi i casi il chiamante riceve BudgetEsaurito, e l'interfaccia passa
alle risposte precalcolate dicendolo.
"""

from __future__ import annotations

import os
import threading

# Prezzi per milione di token, Claude Sonnet 4.5. Sono qui e non sparsi nel
# codice perche' cambiano: se cambiano e nessuno aggiorna, la stima sbaglia in
# silenzio. Meglio un posto solo, dichiarato.
PREZZO_INGRESSO = 3.0
PREZZO_USCITA = 15.0

# Tetto in dollari per istanza. Zero o assente = nessun freno locale.
TETTO = float(os.environ.get("BUDGET_MAX_USD", "0") or 0)


class BudgetEsaurito(Exception):
    """Il budget e' finito, o l'API ha detto che lo e'.

    Non e' un errore da mostrare: e' il segnale che l'interfaccia deve passare
    alle risposte precalcolate.
    """

    def __init__(self, motivo: str, speso: float | None = None):
        self.motivo = motivo
        self.speso = speso
        super().__init__(motivo)


class Contatore:
    """Somma la spesa stimata. Thread-safe perche' i giudici girano in parallelo."""

    def __init__(self, tetto: float = TETTO):
        self.tetto = tetto
        self._speso = 0.0
        self._lock = threading.Lock()

    @property
    def speso(self) -> float:
        return self._speso

    def residuo(self) -> float:
        return float("inf") if not self.tetto else max(0.0, self.tetto - self._speso)

    def verifica(self, stima_ingresso: int = 8000, stima_uscita: int = 400) -> None:
        """Da chiamare PRIMA della richiesta: se non ci sta, non partiamo."""
        if not self.tetto:
            return
        costo = (stima_ingresso / 1e6 * PREZZO_INGRESSO
                 + stima_uscita / 1e6 * PREZZO_USCITA)
        if self._speso + costo > self.tetto:
            raise BudgetEsaurito("tetto di spesa raggiunto", self._speso)

    def registra(self, token_ingresso: int, token_uscita: int) -> float:
        """Da chiamare DOPO, con i token veri riportati dalla risposta."""
        costo = (token_ingresso / 1e6 * PREZZO_INGRESSO
                 + token_uscita / 1e6 * PREZZO_USCITA)
        with self._lock:
            self._speso += costo
        return costo


# Un contatore per processo. In serverless significa uno per istanza calda.
contatore = Contatore()


# ---------------------------------------------------------------- errori API

# Cosa risponde l'API quando il muro c'e' davvero. 402 e' l'unico codice
# documentato per i problemi di fatturazione; 429 copre i rate limit del
# workspace. Le stringhe servono ai client che sollevano eccezioni generiche
# senza esporre lo status.
CODICI_ESAURIMENTO = {402, 429}
SPIE = ("billing_error", "credit balance", "rate_limit_error",
        "insufficient", "quota", "spend limit")


def e_esaurimento(errore: BaseException) -> str | None:
    """L'eccezione dice che siamo a secco? Se si', restituisce il motivo."""
    stato = (getattr(errore, "status_code", None)
             or getattr(getattr(errore, "response", None), "status_code", None))
    if stato in CODICI_ESAURIMENTO:
        return "credito esaurito" if stato == 402 else "troppe richieste"
    testo = str(errore).lower()
    for spia in SPIE:
        if spia in testo:
            return "credito esaurito" if spia != "rate_limit_error" else "troppe richieste"
    return None


def protetta(fn, *args, **kwargs):
    """Esegue una chiamata al modello traducendo l'esaurimento in BudgetEsaurito.

    Qualunque altro errore passa: un guasto vero non deve travestirsi da
    budget finito, altrimenti la demo mente su cosa e' successo.
    """
    contatore.verifica()
    try:
        risposta = fn(*args, **kwargs)
    except BaseException as exc:
        motivo = e_esaurimento(exc)
        if motivo:
            raise BudgetEsaurito(motivo, contatore.speso) from exc
        raise
    ingresso = getattr(risposta, "prompt_tokens_used", None) or 0
    uscita = getattr(risposta, "completion_tokens_used", None) or 0
    if ingresso or uscita:
        contatore.registra(int(ingresso), int(uscita))
    return risposta
