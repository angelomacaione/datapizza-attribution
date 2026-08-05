"""
Due ruoli, due client, due prompt che non si conoscono.

L'estensore scrive la risposta. Il giudice valuta una frase alla volta senza
sapere come e' stata prodotta, senza vedere la domanda originale e senza vedere
il resto della risposta. La separazione non e' cosmetica: se chiedessimo
all'estensore "quali parti ti sei inventato" otterremmo un'autodichiarazione,
cioe' esattamente la cosa di cui questo progetto dice che non ci si puo' fidare.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from datapizza.clients.anthropic import AnthropicClient

ROOT = Path(__file__).resolve().parents[3]

MODEL_ESTENSORE = "claude-sonnet-4-5-20250929"
MODEL_GIUDICE = "claude-sonnet-4-5-20250929"

# ---------------------------------------------------------------- chiave

def load_key() -> str:
    """Legge la chiave da ambiente o da .env. Non la stampa mai."""
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if key:
        return key
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("ANTHROPIC_API_KEY=") and not line.startswith("#"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("ANTHROPIC_API_KEY assente: mettila in .env nella radice del repo")


# ---------------------------------------------------------------- prompt

SISTEMA_ESTENSORE = """Sei l'assistente documentale del progetto Prometeo Cup: una partita di calcio fra robot organizzata alla Fiera di Roma il 21 novembre 2026, con la squadra SPQR Sapienza, robot K1 di Booster Robotics e NAO di riserva.

Rispondi ESCLUSIVAMENTE sulla base dei passaggi che ti vengono forniti. Non usare conoscenza tua sul mondo, sull'azienda o sulla robotica in generale: l'archivio e' l'unica fonte ammessa.

Se i passaggi non contengono l'informazione richiesta, dillo apertamente in una frase e fermati. Non colmare i vuoti con inferenze plausibili, non stimare, non generalizzare da casi simili.

Scrivi in italiano, in modo asciutto e concreto. Da tre a sei frasi. Riporta cifre, date e nomi esattamente come compaiono nei passaggi. Non inserire citazioni, numeri di nota o riferimenti: l'apparato di verifica viene costruito a parte."""

SISTEMA_GIUDICE = """Sei un verificatore. Ricevi UNA affermazione e un elenco di passaggi estratti da un archivio. Devi stabilire se quei passaggi sostengono quella affermazione.

Non sai come l'affermazione sia stata prodotta, e non ti riguarda. Non usare conoscenza tua: l'unica prova ammessa sono i passaggi che vedi.

Tre esiti possibili:

- "supportato": i passaggi affermano il contenuto dell'affermazione, in modo diretto o per composizione evidente di piu' passaggi.
- "contraddetto": i passaggi parlano di questo tema e dicono qualcosa di incompatibile con l'affermazione.
- "non_trattato": i passaggi non affrontano l'affermazione. Sono su argomenti vicini, magari citano le stesse persone o la stessa azienda, ma non dicono nulla su cio' che l'affermazione sostiene.

La distinzione fra "contraddetto" e "non_trattato" e' la piu' importante e la piu' facile da sbagliare. Somiglianza di argomento non e' copertura: se un passaggio parla di riparazioni ai robot di un'azienda, non sta dicendo nulla sul fatturato di quell'azienda.

Nel dubbio scegli "non_trattato". Un falso "supportato" e' l'errore piu' grave che puoi commettere.

In "citazione" riporta VERBATIM il frammento di passaggio che sostiene l'affermazione, copiato carattere per carattere. Se nessun frammento la sostiene alla lettera, lascia la stringa vuota."""


@lru_cache(maxsize=2)
def estensore() -> AnthropicClient:
    return AnthropicClient(api_key=load_key(), model=MODEL_ESTENSORE,
                           system_prompt=SISTEMA_ESTENSORE, temperature=0.0)


@lru_cache(maxsize=2)
def giudice() -> AnthropicClient:
    return AnthropicClient(api_key=load_key(), model=MODEL_GIUDICE,
                           system_prompt=SISTEMA_GIUDICE, temperature=0.0)
