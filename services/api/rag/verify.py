"""
Il verificatore: da una risposta ai quattro stati, frase per frase.

Due passaggi indipendenti che non conoscono il ragionamento di chi ha risposto.

1. Ancoraggio letterale — calcolo puro, nessun modello. Cerca la piu' lunga
   sovrapposizione verbatim fra la frase e i passaggi recuperati. Se esiste,
   abbiamo anche le coordinate esatte da evidenziare nel pannello fonti.

2. Giudizio di implicazione — una chiamata separata che vede solo la frase e i
   passaggi.

Incrociandoli escono quattro stati. Il quarto, "fuori corpus", e' quello che
manca in tutti i sistemi di citazione che ho visto: distingue "l'archivio dice
il contrario" da "l'archivio non ne parla e il modello ha riempito il vuoto".
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Literal

from pydantic import BaseModel, Field

from .llm import giudice
from .retrieve import Hit

# Sotto queste soglie una coincidenza testuale e' casuale, non una citazione.
MIN_SPAN_CHARS = 24
MIN_SPAN_TOKENS = 4

STOPWORD = {
    "il", "lo", "la", "i", "gli", "le", "un", "uno", "una", "di", "a", "da", "in",
    "con", "su", "per", "tra", "fra", "del", "della", "dei", "delle", "dal", "nel",
    "nella", "che", "e", "ed", "o", "ma", "se", "non", "si", "sono", "stato", "essere",
    "come", "piu", "anche", "al", "allo", "alla", "ai", "agli", "alle", "sul", "sulla",
}

STATI = Literal["ripescato", "inferito", "non_supportato", "fuori_corpus"]


class VerdettoGiudice(BaseModel):
    """Schema imposto al giudice: niente prosa libera da riparsare."""
    esito: Literal["supportato", "contraddetto", "non_trattato"] = Field(
        description="supportato se i passaggi affermano il contenuto; contraddetto se "
                    "lo negano; non_trattato se non ne parlano affatto")
    passaggi: list[int] = Field(
        default_factory=list,
        description="numeri dei passaggi usati, come compaiono nell'elenco")
    citazione: str = Field(
        default="",
        description="frammento verbatim che sostiene l'affermazione, vuoto se non esiste")
    motivo: str = Field(description="una frase sul perche', in italiano")
    confidenza: float = Field(ge=0.0, le=1.0, description="quanto sei sicuro dell'esito")


@dataclass
class Ancora:
    """Una sovrapposizione verbatim fra la frase e un passaggio."""
    chunk_id: str
    citazione: str
    citation_label: str
    inizio_nel_chunk: int
    fine_nel_chunk: int
    inizio_nel_file: int
    fine_nel_file: int
    source_file: str


@dataclass
class Affermazione:
    testo: str
    stato: STATI
    confidenza: float
    motivo: str
    ancora: Ancora | None = None
    passaggi: list[dict] = field(default_factory=list)
    citazione_fantasma: str = ""   # il giudice ha citato qualcosa che non esiste

    @property
    def colore(self) -> str:
        return {"ripescato": "verde", "inferito": "blu",
                "non_supportato": "rosso", "fuori_corpus": "arancione"}[self.stato]


# ------------------------------------------------------- ancoraggio letterale

def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s)


def _significativa(frammento: str) -> bool:
    tok = [t for t in re.findall(r"[a-z0-9àèéìòù]+", frammento.lower()) if t not in STOPWORD]
    return len(tok) >= MIN_SPAN_TOKENS


def trova_ancora(frase: str, hits: list[Hit]) -> Ancora | None:
    """Il piu' lungo frammento verbatim condiviso fra la frase e un passaggio.

    Lavora su testo normalizzato per non farsi fermare da accenti e spazi, poi
    riporta gli indici sul testo originale del chunk e sul file sorgente.
    """
    migliore = None
    frase_n = _norm(frase)
    for h in hits:
        testo = h.chunk.text
        testo_n = _norm(testo)
        m = SequenceMatcher(None, frase_n, testo_n, autojunk=False).find_longest_match(
            0, len(frase_n), 0, len(testo_n))
        if m.size < MIN_SPAN_CHARS:
            continue
        frammento_n = testo_n[m.b:m.b + m.size].strip()
        if not _significativa(frammento_n):
            continue
        if migliore is None or m.size > migliore[0]:
            migliore = (m.size, h, m.b, m.b + m.size)

    if migliore is None:
        return None

    _, h, b0, b1 = migliore
    testo = h.chunk.text
    # riallinea gli indici dal testo normalizzato a quello originale
    inizio = _riallinea(testo, b0)
    fine = _riallinea(testo, b1)
    meta = h.chunk.metadata or {}
    base = int(meta.get("start", 0))
    return Ancora(
        chunk_id=h.chunk.id,
        citazione=testo[inizio:fine].strip(),
        citation_label=meta.get("citation", ""),
        inizio_nel_chunk=inizio,
        fine_nel_chunk=fine,
        inizio_nel_file=base + inizio,
        fine_nel_file=base + fine,
        source_file=meta.get("source_file", ""),
    )


def verifica_citazione(citazione: str, hits: list[Hit]) -> Ancora | None:
    """Il frammento che il giudice dice di aver letto esiste davvero?

    E' questo, e non la sovrapposizione con la frase di risposta, a decidere lo
    stato "ripescato". Una risposta scritta bene non copia mai alla lettera: se
    pretendessimo il verbatim dalla risposta, il verde non scatterebbe mai. Il
    giudice invece cita dal passaggio, e quella citazione si puo' confrontare
    carattere per carattere col corpus.

    Effetto collaterale non secondario: se il frammento NON si trova, abbiamo
    beccato un giudice che si e' inventato una prova.
    """
    if len(citazione.strip()) < MIN_SPAN_CHARS or not _significativa(citazione):
        return None
    ago = _norm(citazione).strip()
    for h in hits:
        testo = h.chunk.text
        pos = _norm(testo).find(ago)
        if pos < 0:
            continue
        inizio, fine = _riallinea(testo, pos), _riallinea(testo, pos + len(ago))
        meta = h.chunk.metadata or {}
        base = int(meta.get("start", 0))
        return Ancora(
            chunk_id=h.chunk.id,
            citazione=testo[inizio:fine].strip(),
            citation_label=meta.get("citation", ""),
            inizio_nel_chunk=inizio,
            fine_nel_chunk=fine,
            inizio_nel_file=base + inizio,
            fine_nel_file=base + fine,
            source_file=meta.get("source_file", ""),
        )
    return None


def _riallinea(originale: str, indice_normalizzato: int) -> int:
    """Dall'indice sul testo normalizzato a quello sul testo originale.

    La normalizzazione collassa spazi e toglie accenti, quindi le due stringhe
    hanno lunghezze diverse: bisogna ricamminare in parallelo.
    """
    i_orig = i_norm = 0
    prev_space = False
    while i_orig < len(originale) and i_norm < indice_normalizzato:
        c = originale[i_orig]
        n = _norm(c)
        if c.isspace():
            if not prev_space:
                i_norm += 1
            prev_space = True
        else:
            prev_space = False
            i_norm += len(n)
        i_orig += 1
    return i_orig


# ------------------------------------------------------- spezzare la risposta

def spezza_in_affermazioni(risposta: str) -> list[str]:
    """Una riga di elenco o di tabella e' un'affermazione; il resto va a frasi."""
    pezzi: list[str] = []
    for blocco in risposta.splitlines():
        blocco = blocco.strip()
        if not blocco:
            continue
        if re.match(r"^([-*•]|\d+[.)]|\|)", blocco):
            pezzi.append(blocco.lstrip("-*•").strip())
            continue
        for frase in re.split(r"(?<=[.!?])\s+(?=[A-ZÀÈÉÌÒÙ0-9])", blocco):
            frase = frase.strip()
            if len(frase) > 15:
                pezzi.append(frase)
    return pezzi


# ------------------------------------------------------- verifica

def _passaggi_testo(hits: list[Hit]) -> str:
    righe = []
    for i, h in enumerate(hits, 1):
        m = h.chunk.metadata or {}
        righe.append(f"[{i}] ({m.get('citation','')})\n{h.chunk.text}")
    return "\n\n".join(righe)


def verifica_affermazione(frase: str, hits: list[Hit]) -> Affermazione:
    prompt = (f"AFFERMAZIONE DA VERIFICARE:\n{frase}\n\n"
              f"PASSAGGI DISPONIBILI:\n\n{_passaggi_testo(hits)}")
    # structured_response restituisce un ClientResponse: il modello validato sta
    # in .structured_data, che a seconda della versione e' gia' l'oggetto oppure
    # il dizionario da cui costruirlo.
    risposta = giudice().structured_response(input=prompt, output_cls=VerdettoGiudice)
    dati = getattr(risposta, "structured_data", risposta)
    if isinstance(dati, list):
        dati = dati[0]
    v = dati if isinstance(dati, VerdettoGiudice) else VerdettoGiudice.model_validate(dati)

    # Due ancore possibili: il frammento citato dal giudice (la via normale) o
    # una sovrapposizione verbatim con la frase stessa (rara, ma gratis).
    ancora = verifica_citazione(v.citazione, hits) or trova_ancora(frase, hits)
    fantasma = ""
    if v.citazione.strip() and ancora is None:
        fantasma = v.citazione.strip()

    if v.esito == "non_trattato":
        stato = "fuori_corpus"
    elif v.esito == "contraddetto":
        stato = "non_supportato"
    elif ancora is not None:
        stato = "ripescato"
    else:
        stato = "inferito"

    usati = []
    for n in v.passaggi:
        if 1 <= n <= len(hits):
            m = hits[n - 1].chunk.metadata or {}
            usati.append({"citation": m.get("citation", ""),
                          "register": m.get("register", ""),
                          "chunk_id": hits[n - 1].chunk.id})

    return Affermazione(testo=frase, stato=stato, confidenza=v.confidenza,
                        motivo=v.motivo, ancora=ancora, passaggi=usati,
                        citazione_fantasma=fantasma)


def verifica_risposta(risposta: str, hits: list[Hit]) -> list[Affermazione]:
    return [verifica_affermazione(f, hits) for f in spezza_in_affermazioni(risposta)]
