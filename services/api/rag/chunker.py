"""
Chunker markdown-aware per il vault Prometeo Cup.

Principio: NON tagliamo a finestre cieche. Ogni chunk e' un'unita' comunicativa
reale (un messaggio email, una riga di chat, una decisione di meeting, una
telefonata) e porta con se' chi parla, quando, su quale canale e con quale
registro. La citazione che ne esce e' "email-threads > Thread #28 > Valeria
De Santis, 23 ott 11:22", non "pagina 8".

Ogni chunk conserva gli offset di carattere nel file sorgente: servono al
pannello fonti per evidenziare lo span esatto invece di ri-cercare il testo.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass, field, asdict
from pathlib import Path

# ---------------------------------------------------------------- costanti

# Registro comunicativo per canale. Conta per la demo: una decisione presa via
# email non pesa come un mugugno su WhatsApp alle 00:47, e il pannello fonti
# deve poterlo dire.
REGISTER_BY_CHANNEL = {
    "email-threads": "formale",
    "remote-meetings": "formale",
    "phone-calls": "semi-formale",
    "llm-chats": "semi-formale",
    "web-searches": "semi-formale",
    "colleague-chats": "informale",
}

# Sotto-canali informali riconosciuti dentro colleague-chats.
INFORMAL_MARKERS = ("whatsapp", "random", "telegram", "dm ")

MONTHS = {
    "gen": 1, "feb": 2, "mar": 3, "apr": 4, "mag": 5, "giu": 6,
    "lug": 7, "ago": 8, "set": 9, "ott": 10, "nov": 11, "dic": 12,
    "gennaio": 1, "febbraio": 2, "marzo": 3, "aprile": 4, "maggio": 5,
    "giugno": 6, "luglio": 7, "agosto": 8, "settembre": 9, "ottobre": 10,
    "novembre": 11, "dicembre": 12,
}

MAX_CHARS = 1400   # oltre questa soglia un chunk viene spezzato
MIN_CHARS = 60     # sotto questa soglia non vale come chunk autonomo


# ---------------------------------------------------------------- modello

@dataclass
class Chunk:
    id: str
    text: str
    channel: str
    section: str
    subsection: str | None
    speaker: str | None
    addressee: str | None
    timestamp: str | None      # ISO se ricostruibile
    timestamp_raw: str | None  # come appare nel testo
    register: str
    kind: str                  # email_message | chat_line | decision | call | llm_turn | note | prose
    start: int                 # offset di carattere nel file sorgente
    end: int
    source_file: str
    entities: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def citation(self) -> str:
        bits = [self.channel, self.section]
        if self.subsection:
            bits.append(self.subsection)
        who = self.speaker or ""
        when = self.timestamp_raw or ""
        tail = " ".join(x for x in (who, when) if x).strip()
        if tail:
            bits.append(tail)
        return " > ".join(bits)


# ---------------------------------------------------------------- utilita'

def _slug(text: str, n: int = 8) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def _iso(day: str | None, month: str | None, time: str | None,
         default_year: int = 2026) -> str | None:
    """Ricostruisce un ISO dai formati sparsi del vault ('22 ott, 09:14')."""
    if not day or not month:
        return None
    m = MONTHS.get(_norm(month)[:3])
    if not m:
        return None
    try:
        d = int(day)
    except ValueError:
        return None
    # Il vault copre 21 ottobre -> 21 novembre 2026.
    hh, mm = (time.split(":") + ["00"])[:2] if time else ("00", "00")
    try:
        return f"{default_year:04d}-{m:02d}-{d:02d}T{int(hh):02d}:{int(mm):02d}"
    except ValueError:
        return None


def _clean(text: str) -> str:
    """Toglie la decorazione markdown che sporca il retrieval, tiene il senso."""
    out = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("```"):              # recinti di codice: fuori dall'indice
            continue
        s = re.sub(r"^>\s?", "", s)          # blockquote
        s = re.sub(r"^[-*]\s+", "- ", s)     # bullet uniformi
        out.append(s)
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _split_long(text: str, limit: int = MAX_CHARS) -> list[tuple[str, int]]:
    """Spezza un blocco lungo su confini di riga.

    Ritorna (pezzo_grezzo, offset_relativo) SENZA ripulire: gli offset devono
    restare validi sul file sorgente, altrimenti l'evidenziazione nel pannello
    fonti punta al posto sbagliato.
    """
    if len(text) <= limit:
        return [(text, 0)]
    parts, buf, buf_start, cursor = [], [], 0, 0
    for line in text.splitlines(keepends=True):
        if buf and sum(len(x) for x in buf) + len(line) > limit:
            parts.append(("".join(buf), buf_start))
            buf, buf_start = [], cursor
        buf.append(line)
        cursor += len(line)
    if buf:
        parts.append(("".join(buf), buf_start))
    return parts


# ---------------------------------------------------------------- entita'

def load_entities(index_path: Path) -> list[str]:
    """Legge i nomi entita' dai wikilink di 00-Index.md."""
    if not index_path.exists():
        return []
    text = index_path.read_text(encoding="utf-8")
    names = re.findall(r"\[\[([^\]]+)\]\]", text)
    # scarta i 6 canali, non sono entita'
    return sorted({n for n in names if n not in REGISTER_BY_CHANNEL})


def tag_entities(text: str, entities: list[str]) -> list[str]:
    """Match delle entita' note nel testo. Usa il nome base senza parentesi."""
    norm_text = _norm(text)
    found = []
    for e in entities:
        base = re.sub(r"\s*\([^)]*\)", "", e).strip()
        if len(base) < 4:
            continue
        if _norm(base) in norm_text:
            found.append(e)
        else:
            # cognome/nome singolo, per catturare "Federica" o "Vincenzo"
            first = base.split()[0]
            if len(first) >= 5 and _norm(first) in norm_text:
                found.append(e)
    return sorted(set(found))


# ---------------------------------------------------------------- sezioni

@dataclass
class Section:
    title: str
    body: str
    start: int      # offset assoluto del corpo nel file
    level: int


def split_sections(text: str, level: int = 2) -> list[Section]:
    """Divide su heading di un dato livello, conservando gli offset assoluti."""
    marker = "#" * level
    pattern = re.compile(rf"^{marker} (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    sections: list[Section] = []
    for i, m in enumerate(matches):
        body_start = m.end() + 1
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections.append(Section(
            title=m.group(1).strip(),
            body=text[body_start:body_end],
            start=body_start,
            level=level,
        ))
    return sections


# ---------------------------------------------------------- estrattori

# **[22 ott, 09:14] Luca Ferraresi → thread**
RE_EMAIL_MSG = re.compile(
    r"^\*\*\[(?P<day>\d{1,2})\s+(?P<month>[a-zA-Zàèéìòù]+),?\s*(?P<time>\d{1,2}:\d{2})\]\s*"
    r"(?P<speaker>[^→\]]+?)\s*→\s*(?P<to>[^*]+?)\*\*\s*$",
    re.MULTILINE,
)

# 09:17  [Luca]        Booting K1 series
RE_CHAT_LINE = re.compile(r"^(?P<time>\d{2}:\d{2})\s+\[(?P<speaker>[^\]]+)\]\s*(?P<text>.*)$")

# > **Federica**: testo
RE_LLM_TURN = re.compile(r"^>\s*\*\*(?P<speaker>[^*]+)\*\*:\s*(?P<text>.+)$", re.MULTILINE)

# ## ☎️ Luca Ferraresi → Vincenzo Suriani · 26 ott 2026, 22:17
RE_CALL_HEAD = re.compile(
    r"(?P<caller>[^→]+)→\s*(?P<callee>[^·]+)·\s*(?P<day>\d{1,2})\s+(?P<month>[a-zA-Zàèéìòù]+)"
    r"(?:\s+\d{4})?,?\s*(?P<time>\d{1,2}:\d{2})?"
)

# ## Thread #28 — "titolo"  /  ## 2. DR2 — Briefing ... — mercoledì 28 ottobre 2026, 14:00
RE_DATE_IN_TITLE = re.compile(
    r"(?P<day>\d{1,2})\s+(?P<month>gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|"
    r"agosto|settembre|ottobre|novembre|dicembre|gen|feb|mar|apr|mag|giu|lug|ago|set|ott|nov|dic)"
    r"(?:\s+\d{4})?(?:,?\s*(?P<time>\d{1,2}:\d{2}))?",
    re.IGNORECASE,
)


def _register_for(channel: str, section_title: str) -> str:
    base = REGISTER_BY_CHANNEL.get(channel, "semi-formale")
    if channel == "colleague-chats":
        low = _norm(section_title)
        if any(mk in low for mk in INFORMAL_MARKERS):
            return "informale"
        return "informale"
    return base


def _mk(text_raw: str, abs_start: int, *, channel: str, section: str,
        subsection: str | None, speaker: str | None, addressee: str | None,
        ts: str | None, ts_raw: str | None, kind: str, source_file: str,
        entities: list[str]) -> list[Chunk]:
    """Fabbrica uno o piu' chunk da un blocco, spezzando se troppo lungo.

    `text` finisce nell'indice ed e' ripulito dal markup; `start`/`end` restano
    ancorati al testo GREZZO del file, cosi' il pannello fonti evidenzia lo span
    reale invece di andare a ricercare la stringa.
    """
    chunks = []
    for raw_piece, rel in _split_long(text_raw):
        lead = len(raw_piece) - len(raw_piece.lstrip())
        raw_core = raw_piece.strip()
        piece = _clean(raw_core)
        if len(piece) < MIN_CHARS:
            continue
        span_start = abs_start + rel + lead
        cid = f"{channel}:{_slug(f'{source_file}{span_start}{piece[:40]}')}"
        chunks.append(Chunk(
            id=cid,
            text=piece,
            channel=channel,
            section=section,
            subsection=subsection,
            speaker=speaker,
            addressee=addressee,
            timestamp=ts,
            timestamp_raw=ts_raw,
            register=_register_for(channel, section),
            kind=kind,
            start=span_start,
            end=span_start + len(raw_core),
            source_file=source_file,
            entities=tag_entities(piece, entities),
        ))
    return chunks


def chunk_email(sec: Section, channel: str, src: str, ents: list[str]) -> list[Chunk]:
    out: list[Chunk] = []
    msgs = list(RE_EMAIL_MSG.finditer(sec.body))
    if not msgs:
        return chunk_prose(sec, channel, src, ents)
    # la sintesi che precede il primo messaggio vale come chunk a se'
    head = sec.body[: msgs[0].start()]
    out += _mk(head, sec.start, channel=channel, section=sec.title, subsection="Sintesi",
               speaker=None, addressee=None, ts=None, ts_raw=None, kind="prose",
               source_file=src, entities=ents)
    for i, m in enumerate(msgs):
        body_start = m.end() + 1
        body_end = msgs[i + 1].start() if i + 1 < len(msgs) else len(sec.body)
        ts_raw = f"{m.group('day')} {m.group('month')} {m.group('time')}"
        out += _mk(
            sec.body[body_start:body_end], sec.start + body_start,
            channel=channel, section=sec.title, subsection=None,
            speaker=m.group("speaker").strip(), addressee=m.group("to").strip(),
            ts=_iso(m.group("day"), m.group("month"), m.group("time")),
            ts_raw=ts_raw, kind="email_message", source_file=src, entities=ents,
        )
    return out


def chunk_chat(sec: Section, channel: str, src: str, ents: list[str]) -> list[Chunk]:
    """Chat: raggruppa righe consecutive in finestre coerenti, non una per riga.

    Una riga sola ('K1-02 green') non e' recuperabile ne' citabile in modo utile.
    Raggruppiamo per prossimita' mantenendo la lista degli speaker.
    """
    out: list[Chunk] = []
    body = sec.body
    offset = 0
    win_start: int | None = None
    win_end = 0
    win_speakers: list[str] = []
    win_first_time: str | None = None

    def flush():
        """Emette la finestra come fetta CONTIGUA del corpo.

        Contigua e' la parola importante: se ricomponessimo il blob saltando i
        recinti ``` la lunghezza non corrisponderebbe piu' al sorgente e
        l'evidenziazione punterebbe altrove. I recinti li toglie _clean.
        """
        nonlocal win_start, win_end, win_speakers, win_first_time
        if win_start is not None and win_end > win_start:
            speakers = ", ".join(dict.fromkeys(win_speakers)) or None
            out.extend(_mk(
                body[win_start:win_end], sec.start + win_start, channel=channel,
                section=sec.title, subsection=None, speaker=speakers, addressee=None,
                ts=None, ts_raw=win_first_time, kind="chat_line", source_file=src,
                entities=ents,
            ))
        win_start, win_speakers, win_first_time = None, [], None

    for line in body.splitlines(keepends=True):
        stripped = line.strip()
        size = win_end - (win_start if win_start is not None else win_end)
        if stripped.startswith("```"):
            offset += len(line)
            continue
        m = RE_CHAT_LINE.match(stripped)
        if m:
            if win_start is None:
                win_start = offset
            if win_first_time is None:
                win_first_time = m.group("time")
            win_speakers.append(m.group("speaker").strip())
            win_end = offset + len(line)
            if win_end - win_start > 900:
                flush()
        elif stripped:
            if win_start is None:
                win_start = offset
            win_end = offset + len(line)
        else:
            if win_start is not None and size > 400:
                flush()
        offset += len(line)
    flush()
    return out


def chunk_call(sec: Section, channel: str, src: str, ents: list[str]) -> list[Chunk]:
    m = RE_CALL_HEAD.search(sec.title)
    caller = callee = ts = ts_raw = None
    if m:
        caller = m.group("caller").replace("☎️", "").strip()
        callee = m.group("callee").strip()
        ts = _iso(m.group("day"), m.group("month"), m.group("time"))
        ts_raw = f"{m.group('day')} {m.group('month')}" + (
            f" {m.group('time')}" if m.group("time") else "")
    return _mk(sec.body, sec.start, channel=channel, section=sec.title, subsection=None,
               speaker=caller, addressee=callee, ts=ts, ts_raw=ts_raw, kind="call",
               source_file=src, entities=ents)


def chunk_meeting(sec: Section, channel: str, src: str, ents: list[str]) -> list[Chunk]:
    """Meeting: le sotto-sezioni sono unita' diverse. Le Decisioni si spezzano
    voce per voce: sono le affermazioni 'firmate', quelle su cui si delibera."""
    out: list[Chunk] = []
    dm = RE_DATE_IN_TITLE.search(sec.title)
    ts = _iso(dm.group("day"), dm.group("month"), dm.group("time")) if dm else None
    ts_raw = dm.group(0) if dm else None

    subs = split_sections(sec.body, level=3)
    if not subs:
        return _mk(sec.body, sec.start, channel=channel, section=sec.title,
                   subsection=None, speaker=None, addressee=None, ts=ts,
                   ts_raw=ts_raw, kind="prose", source_file=src, entities=ents)

    head = sec.body[: subs[0].start] if subs else ""
    out += _mk(head, sec.start, channel=channel, section=sec.title, subsection="Intestazione",
               speaker=None, addressee=None, ts=ts, ts_raw=ts_raw, kind="prose",
               source_file=src, entities=ents)

    for sub in subs:
        abs_start = sec.start + sub.start
        is_decision = _norm(sub.title).startswith(("decision", "action"))
        if is_decision:
            # una voce = un chunk
            items = re.split(r"^(?=\d+\.\s|\-\s)", sub.body, flags=re.MULTILINE)
            cursor = 0
            for it in items:
                if it.strip():
                    out += _mk(it, abs_start + cursor, channel=channel, section=sec.title,
                               subsection=sub.title, speaker=None, addressee=None, ts=ts,
                               ts_raw=ts_raw, kind="decision", source_file=src, entities=ents)
                cursor += len(it)
        else:
            out += _mk(sub.body, abs_start, channel=channel, section=sec.title,
                       subsection=sub.title, speaker=None, addressee=None, ts=ts,
                       ts_raw=ts_raw, kind="prose", source_file=src, entities=ents)
    return out


def chunk_llm(sec: Section, channel: str, src: str, ents: list[str]) -> list[Chunk]:
    """llm-chats: la sezione e' la persona, la sotto-sezione la sessione.

    Le righe '**Nota**:' sono annotazioni editoriali fuori-narrazione: le
    marchiamo, perche' leggerle come fatto e' esattamente il tipo di errore
    che questa demo deve saper mostrare.
    """
    out: list[Chunk] = []
    person = sec.title.split("—")[0].strip(" 🎯🤖📣🏥💬")
    subs = split_sections(sec.body, level=3)
    if not subs:
        return _mk(sec.body, sec.start, channel=channel, section=sec.title, subsection=None,
                   speaker=person, addressee=None, ts=None, ts_raw=None, kind="prose",
                   source_file=src, entities=ents)
    for sub in subs:
        abs_start = sec.start + sub.start
        dm = RE_DATE_IN_TITLE.search(sub.title)
        ts = _iso(dm.group("day"), dm.group("month"), dm.group("time")) if dm else None
        ts_raw = dm.group(0) if dm else None
        # Taglio contiguo alla prima riga '**Nota**': cosi' i due pezzi restano
        # fette esatte del sorgente e gli offset reggono.
        nm = re.search(r"^\*\*Nota\*\*", sub.body, re.MULTILINE)
        note_off = nm.start() if nm else len(sub.body)
        out += _mk(sub.body[:note_off], abs_start, channel=channel, section=sec.title,
                   subsection=sub.title, speaker=person, addressee=None, ts=ts,
                   ts_raw=ts_raw, kind="llm_turn", source_file=src, entities=ents)
        if nm:
            out += _mk(sub.body[note_off:], abs_start + note_off, channel=channel,
                       section=sec.title, subsection=sub.title, speaker="[annotazione]",
                       addressee=None, ts=ts, ts_raw=ts_raw, kind="note",
                       source_file=src, entities=ents)
    return out


def chunk_prose(sec: Section, channel: str, src: str, ents: list[str]) -> list[Chunk]:
    subs = split_sections(sec.body, level=3)
    if not subs:
        return _mk(sec.body, sec.start, channel=channel, section=sec.title, subsection=None,
                   speaker=None, addressee=None, ts=None, ts_raw=None, kind="prose",
                   source_file=src, entities=ents)
    out: list[Chunk] = []
    head = sec.body[: subs[0].start]
    out += _mk(head, sec.start, channel=channel, section=sec.title, subsection=None,
               speaker=None, addressee=None, ts=None, ts_raw=None, kind="prose",
               source_file=src, entities=ents)
    for sub in subs:
        out += _mk(sub.body, sec.start + sub.start, channel=channel, section=sec.title,
                   subsection=sub.title, speaker=None, addressee=None, ts=None,
                   ts_raw=None, kind="prose", source_file=src, entities=ents)
    return out


DISPATCH = {
    "email-threads": chunk_email,
    "colleague-chats": chunk_chat,
    "phone-calls": chunk_call,
    "remote-meetings": chunk_meeting,
    "llm-chats": chunk_llm,
    "web-searches": chunk_prose,
}


# ---------------------------------------------------------------- entrypoint

def chunk_vault(vault_dir: Path) -> list[Chunk]:
    """Indicizza SOLO channels/.

    Le 75 note in people/organizations/... sono metadato derivato: contengono
    conteggi di menzione e pesi di co-occorrenza, zero prosa. Indicizzarle
    produrrebbe citazioni formalmente perfette e informativamente vuote, che e'
    precisamente il difetto che questa demo denuncia. Restano fuori dall'indice
    e rientrano come grafo di boost.
    """
    entities = load_entities(vault_dir / "00-Index.md")
    chunks: list[Chunk] = []
    for path in sorted((vault_dir / "channels").glob("*.md")):
        channel = path.stem
        text = path.read_text(encoding="utf-8")
        handler = DISPATCH.get(channel, chunk_prose)
        for sec in split_sections(text, level=2):
            chunks.extend(handler(sec, channel, path.name, entities))
    return chunks
