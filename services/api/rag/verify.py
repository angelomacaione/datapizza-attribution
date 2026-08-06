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

from .llm import giudice, revisore
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
    # --- controllo temporale, secondario rispetto al verdetto ---------------
    conflitto_temporale: bool = Field(
        default=False,
        description="esiste fra i passaggi uno piu' recente che cambia questo "
                    "stesso fatto rispetto a quello su cui ti sei basato")
    passaggi_in_conflitto: list[int] = Field(
        default_factory=list,
        description="i due o piu' passaggi che raccontano lo stesso fatto in modo "
                    "diverso in momenti diversi")
    nota_temporale: str = Field(
        default="", description="cosa e' cambiato e in che direzione, una frase")


class EsitoRevisione(BaseModel):
    """Il frammento che mostreremmo all'utente regge da solo?"""
    sufficiente: bool = Field(
        description="il frammento, isolato, giustifica il verdetto emesso")
    motivo: str = Field(description="una frase sul perche', in italiano")


@dataclass
class ConflittoTemporale:
    """Due passaggi veri che dicono cose diverse in momenti diversi.

    Non e' un quinto stato: il colore continua a dire se l'affermazione regge
    sulle prove. Questo dice che le prove sono cambiate nel tempo, e da quando.
    """
    nota: str
    prima: dict
    dopo: dict


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
    conflitto: ConflittoTemporale | None = None
    ancora_scartata: str = ""      # la prova esisteva ma non c'entrava

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
    """I passaggi arrivano al giudice CON LA DATA.

    Senza data due affermazioni incompatibili sembrano un errore dell'archivio;
    con la data si vede che una e' semplicemente successiva all'altra.
    """
    righe = []
    for i, h in enumerate(hits, 1):
        m = h.chunk.metadata or {}
        quando = m.get("timestamp") or m.get("timestamp_raw") or "data ignota"
        righe.append(f"[{i}] {quando} — ({m.get('citation','')})\n{h.chunk.text}")
    return "\n\n".join(righe)


MESI_IT = {"gennaio": 1, "febbraio": 2, "marzo": 3, "aprile": 4, "maggio": 5,
           "giugno": 6, "luglio": 7, "agosto": 8, "settembre": 9, "ottobre": 10,
           "novembre": 11, "dicembre": 12,
           "gen": 1, "feb": 2, "mar": 3, "apr": 4, "mag": 5, "giu": 6, "lug": 7,
           "ago": 8, "set": 9, "ott": 10, "nov": 11, "dic": 12}

RE_DATA_ESTESA = re.compile(
    r"\b(\d{1,2})\s+(" + "|".join(MESI_IT) + r")\b", re.IGNORECASE)
RE_DATA_NUMERICA = re.compile(r"\b(\d{1,2})/(\d{1,2})(?!\d)")


def date_citate(testo: str) -> set[tuple[int, int]]:
    """Le date esplicite in un testo, come coppie (giorno, mese)."""
    fuori: set[tuple[int, int]] = set()
    for g, m in RE_DATA_ESTESA.findall(testo):
        mese = MESI_IT.get(m.lower())
        if mese:
            fuori.add((int(g), mese))
    for g, m in RE_DATA_NUMERICA.findall(testo):
        if 1 <= int(m) <= 12 and 1 <= int(g) <= 31:
            fuori.add((int(g), int(m)))
    return fuori


def _riga_date(frase: str, ancora: Ancora, quando: str) -> str:
    """Confronto fra le date dell'affermazione e quella del frammento.

    Il revisore, a cui il criterio era stato scritto a parole, ha lasciato
    passare un'affermazione datata 28 ottobre ancorata a un passaggio del 31.
    Un confronto fra date pero' e' un calcolo: lo facciamo noi e glielo
    consegniamo gia' fatto, cosi' non puo' distrarsi. La decisione resta sua,
    perche' una data diversa non e' sempre un errore: un documento del 25 puo'
    legittimamente parlare di una scadenza del 27.
    """
    nella_frase = date_citate(frase)
    if not nella_frase:
        return ""
    nel_frammento = date_citate(ancora.citazione)
    data_chunk = ""
    if quando and quando[:10].count("-") == 2:
        try:
            _, mm, dd = quando[:10].split("-")
            data_chunk = f"{int(dd)}/{int(mm)}"
            nel_frammento.add((int(dd), int(mm)))
        except ValueError:
            pass
    mancanti = sorted(nella_frase - nel_frammento)
    if not mancanti:
        return ""
    elenco = ", ".join(f"{g}/{m}" for g, m in mancanti)
    return (f"\n\nVERIFICA AUTOMATICA DELLE DATE\n"
            f"L'affermazione cita: {elenco}. Il frammento e' datato "
            f"{data_chunk or 'ignoto'} e al suo interno quelle date non compaiono.\n"
            f"Valuta se l'affermazione stia collocando il fatto in un momento che il "
            f"frammento non attesta, oppure se la data appartenga legittimamente al "
            f"contenuto (una scadenza futura, un evento programmato).")


def _ancora_pertinente(frase: str, stato: str, ancora: Ancora,
                       hits: list[Hit]) -> tuple[bool, str]:
    """Terzo passaggio: la prova che mostreremmo regge da sola?

    Il controllo verbatim dimostra che la citazione ESISTE, non che C'ENTRI, e
    la differenza fra le due cose ci e' costata tre errori veri:

      · "Nessun altro ruolo il giorno" esibito a sostegno di "nessun'altra
        persona ha accesso al trigger" — parla di Trombetta, non degli altri;
      · un'affermazione datata 28 ottobre ancorata a un passaggio del 31;
      · un'intestazione di telefonata spacciata per contenuto.

    Il revisore vede SOLO il frammento, con la sua data e la sua provenienza:
    e' la stessa cosa che vedrebbe un lettore che clicca. Se a lui non basta,
    non deve bastare a noi.
    """
    meta = next((h.chunk.metadata or {} for h in hits
                 if h.chunk.id == ancora.chunk_id), {})
    quando = meta.get("timestamp") or meta.get("timestamp_raw") or "data ignota"
    prompt = (f"AFFERMAZIONE:\n{frase}\n\n"
              f"VERDETTO EMESSO: {stato}\n\n"
              f"FRAMMENTO CHE VERREBBE MOSTRATO COME PROVA\n"
              f"data: {quando}\nprovenienza: {ancora.citation_label}\n"
              f"testo: \"{ancora.citazione}\""
              + _riga_date(frase, ancora, quando))
    r = revisore().structured_response(input=prompt, output_cls=EsitoRevisione)
    d = getattr(r, "structured_data", r)
    if isinstance(d, list):
        d = d[0]
    e = d if isinstance(d, EsitoRevisione) else EsitoRevisione.model_validate(d)
    return e.sufficiente, e.motivo


def _rileva_conflitto(v: VerdettoGiudice, hits: list[Hit]) -> ConflittoTemporale | None:
    """Ordina il conflitto segnalato dal giudice usando i NOSTRI timestamp.

    Al modello chiediamo solo quali passaggi confliggono. Quale venga prima lo
    decidiamo noi sui metadati: e' un dato che abbiamo, non serve fidarsi.
    """
    if not v.conflitto_temporale or len(v.passaggi_in_conflitto) < 2:
        return None
    scelti = []
    for n in v.passaggi_in_conflitto:
        if 1 <= n <= len(hits):
            m = hits[n - 1].chunk.metadata or {}
            if m.get("timestamp"):
                scelti.append((m["timestamp"], m, hits[n - 1]))
    if len(scelti) < 2:
        return None
    scelti.sort(key=lambda t: t[0])
    (t_pri, m_pri, h_pri), (t_dop, m_dop, h_dop) = scelti[0], scelti[-1]
    if t_pri == t_dop:
        return None

    def scheda(ts, m, h):
        return {"quando": ts, "dove": m.get("citation", ""),
                "file": m.get("source_file", ""), "start": m.get("start"),
                "end": m.get("end"), "registro": m.get("register", ""),
                "estratto": h.chunk.text[:220]}

    return ConflittoTemporale(nota=v.nota_temporale,
                              prima=scheda(t_pri, m_pri, h_pri),
                              dopo=scheda(t_dop, m_dop, h_dop))


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

    # Terzo passaggio: la prova esibita deve reggere isolata. Si applica solo
    # dove una prova viene davvero mostrata, quindi verde e rosso ancorati.
    scartata = ""
    if ancora is not None and stato in ("ripescato", "non_supportato"):
        ok, perche = _ancora_pertinente(frase, stato, ancora, hits)
        if not ok:
            scartata = f"{ancora.citazione} — {perche}"
            ancora = None
            if stato == "ripescato":
                # senza una prova letterale valida non e' piu' "ripescato":
                # l'appoggio puo' esserci, ma non nella forma che mostriamo
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
                        citazione_fantasma=fantasma,
                        conflitto=_rileva_conflitto(v, hits),
                        ancora_scartata=scartata)


def verifica_risposta(risposta: str, hits: list[Hit]) -> list[Affermazione]:
    return [verifica_affermazione(f, hits) for f in spezza_in_affermazioni(risposta)]
