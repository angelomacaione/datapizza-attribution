#!/usr/bin/env python3
"""
Cerca nel corpus i punti in cui l'archivio si contraddice nel tempo.

    python3 scripts/find_contradictions.py [cartella_indice] [--max N]

Non fabbrica trappole: le trova. Il metodo sfrutta l'indice che abbiamo gia',
senza bisogno del modello di embedding, perche' la similarita' fra chunk si
calcola sui vettori salvati.

  1. coppie di chunk che parlano della stessa cosa (similarita' alta)
  2. tenute solo se hanno timestamp diversi e stanno in sezioni diverse
     (dentro lo stesso thread una differenza e' evoluzione, non conflitto)
  3. ogni coppia viene sottoposta a Claude, che deve dire se le due
     affermazioni sono incompatibili e formulare la domanda che porterebbe un
     sistema di retrieval a rispondere con quella sbagliata

Il prodotto sono le domande-trappola: quelle su cui la demo ha qualcosa da
mostrare, perche' nascono da un difetto reale del materiale e non da un
esempio costruito a tavolino.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services" / "api"))

from rag.ambiente import carica_env  # noqa: E402

carica_env()   # .env -> os.environ, cosi' non serve ricordarsi di sourcearlo

from rag.llm import giudice  # noqa: E402
from rag.store import NumpyVectorstore  # noqa: E402

# La media fra chunk qualsiasi e' 0.836, quindi 0.90 sembrava una soglia
# generosa. Non lo era: la contraddizione migliore che conoscevamo (Barbara
# contro Trombetta sul trigger dell'e-stop) sta a 0.8775, cioe' 402a su 8561
# coppie valide, e restava sotto la soglia. Con chunk monotematici la coppia
# risale, ma il margine va tenuto largo lo stesso.
SOGLIA_SIMILARITA = 0.87
MAX_COPPIE = 120


class Conflitto(BaseModel):
    stesso_fatto: bool = Field(description="i due passaggi parlano dello stesso fatto specifico")
    incompatibili: bool = Field(description="cio' che affermano non puo' essere vero insieme")
    fatto: str = Field(description="di quale fatto si tratta, in poche parole")
    dice_prima: str = Field(description="cosa afferma il passaggio piu' vecchio")
    dice_dopo: str = Field(description="cosa afferma il passaggio piu' recente")
    domanda_trappola: str = Field(
        description="una domanda in italiano la cui risposta corretta dipende da quale "
                    "dei due passaggi viene recuperato; deve sembrare innocua")
    gravita: str = Field(description="alta, media o bassa")


ISTRUZIONI = """Ti do due passaggi estratti dallo stesso archivio aziendale, con la data in cui sono stati scritti.

Devi stabilire se raccontano lo stesso fatto specifico in modo incompatibile: un ruolo assegnato a due persone diverse, un numero che cambia, una decisione presa e poi ribaltata, una data spostata.

Non basta che parlino dello stesso argomento. Due passaggi sullo stesso progetto che dicono cose diverse ma compatibili NON sono un conflitto. Un piano che si arricchisce di dettagli non e' un conflitto. Cerco i casi in cui, se un sistema recuperasse solo uno dei due, darebbe una risposta che l'altro smentisce.

Se sono incompatibili, formula la domanda-trappola: una domanda dall'aria normale, che un utente farebbe davvero, e la cui risposta cambia a seconda di quale passaggio viene pescato. Non deve contenere indizi del conflitto.

Attenzione a un errore ricorrente: se il passaggio piu' recente RIPETE o CONFERMA lo stesso valore del piu' vecchio, non c'e' nessun conflitto. Stessa cifra due volte significa coerenza, non contraddizione.

Se non c'e' conflitto metti stesso_fatto o incompatibili a false e lascia il resto vuoto."""


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    index_dir = Path(args[0]) if args else ROOT / "index"
    limite = MAX_COPPIE
    if "--max" in sys.argv:
        limite = int(sys.argv[sys.argv.index("--max") + 1])

    store = NumpyVectorstore.load(index_dir)
    chunks = store.all_chunks()
    M = store._matrix["prometeo"]
    U = M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-10)
    S = U @ U.T
    np.fill_diagonal(S, -1.0)

    meta = [c.metadata or {} for c in chunks]
    candidati = []
    for i in range(len(chunks)):
        for j in range(i + 1, len(chunks)):
            if S[i, j] < SOGLIA_SIMILARITA:
                continue
            ti, tj = meta[i].get("timestamp"), meta[j].get("timestamp")
            if not ti or not tj or ti == tj:
                continue
            if meta[i].get("section") == meta[j].get("section"):
                continue          # stesso thread: e' evoluzione, non conflitto
            a, b = (i, j) if ti <= tj else (j, i)
            candidati.append((float(S[i, j]), a, b))

    candidati.sort(reverse=True)
    candidati = candidati[:limite]
    print(f"chunk: {len(chunks)} · coppie sopra {SOGLIA_SIMILARITA}: {len(candidati)} "
          f"(esaminate: {min(limite, len(candidati))})\n")

    trovati = []
    for sim, a, b in candidati:
        prompt = (
            f"{ISTRUZIONI}\n\n"
            f"PASSAGGIO PIU' VECCHIO — {meta[a].get('timestamp')} — "
            f"{meta[a].get('citation')}\n{chunks[a].text}\n\n"
            f"PASSAGGIO PIU' RECENTE — {meta[b].get('timestamp')} — "
            f"{meta[b].get('citation')}\n{chunks[b].text}")
        r = giudice().structured_response(input=prompt, output_cls=Conflitto)
        d = getattr(r, "structured_data", r)
        if isinstance(d, list):
            d = d[0]
        c = d if isinstance(d, Conflitto) else Conflitto.model_validate(d)
        if not (c.stesso_fatto and c.incompatibili):
            continue
        # Rete di sicurezza: al primo giro un conflitto e' stato dichiarato tale
        # mentre nel campo accanto il modello scriveva "non c'e' conflitto reale
        # sui numeri". Se non sa formulare la trappola o graduare la gravita',
        # il conflitto non c'e'.
        if not c.domanda_trappola.strip() or c.gravita.lower() not in {"alta", "media", "bassa"}:
            print(f"   (scartato: dichiarato conflitto ma senza trappola — {c.fatto[:60]})")
            continue

        trovati.append({
            "similarita": round(sim, 4), "gravita": c.gravita, "fatto": c.fatto,
            "domanda_trappola": c.domanda_trappola,
            "prima": {"quando": meta[a].get("timestamp"), "dove": meta[a].get("citation"),
                      "dice": c.dice_prima, "file": meta[a].get("source_file"),
                      "start": meta[a].get("start"), "end": meta[a].get("end")},
            "dopo": {"quando": meta[b].get("timestamp"), "dove": meta[b].get("citation"),
                     "dice": c.dice_dopo, "file": meta[b].get("source_file"),
                     "start": meta[b].get("start"), "end": meta[b].get("end")},
        })
        print(f"[{c.gravita.upper()}] {c.fatto}   (sim {sim:.3f})")
        print(f"   {meta[a].get('timestamp')}  {c.dice_prima[:96]}")
        print(f"   {meta[b].get('timestamp')}  {c.dice_dopo[:96]}")
        print(f"   trappola: {c.domanda_trappola}\n")

    out = index_dir / "contraddizioni.json"
    out.write_text(json.dumps(trovati, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{len(trovati)} conflitti reali su {len(candidati)} coppie esaminate → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
