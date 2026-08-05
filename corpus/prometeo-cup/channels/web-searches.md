# web-searches.md
**Periodo**: T-1 mese → T-1 giorno (21 ottobre → 20 novembre 2026)
**Canali**:
- Google / Bing — ricerche pubbliche
- Perplexity AI — ricerche con sintesi e citazioni (usata molto da Federica, Tommaso, Elena)
- DuckDuckGo — Luca e Stefano per ricerche anonime
- **RAG interno** — *"Archivio Nereo"* (sistema RAG aziendale su base Azure AI Search, ingerisce: Confluence interno, Drive aziendale, email archiviate, SharePoint, documentazione fornitori). Utilizzato da Valeria, Barbara, Elena, HR.
- **GitHub** / **arXiv** / **Google Scholar** — Luca, Vincenzo, SPQR

**Volume stimato**: circa 1.400 ricerche web nel periodo, 380 query su Archivio Nereo, 220 query su repository tecnici.

Quello che segue è una **selezione rappresentativa** organizzata per Lead, con le query che hanno prodotto insight utile o hanno cambiato una decisione.

---

## 🔍 Federica Mazzarese — Program Director

**Pattern**: Federica usa Perplexity molto più di Google. Query quasi sempre sintattiche lunghe, in italiano, con chiarimento del contesto.

### Ultima settimana ottobre

```
22/10 — "come gestire delta budget +5% in evento corporate senza perdere fiducia CFO"
24/10 — "Amy Edmondson psychological safety frasi ponte italiano"
26/10 — "tempi realistici recupero team dopo dry run fallito parzialmente"
28/10 — "best practice debrief post dry run eventi live tecnologici"
29/10 — "modello decisionale incertezza 30 giorni evento live"
```

### Prima metà novembre

```
02/11 — "evento corporate Presidente istituzionale cerimonia linguaggio non politico"
04/11 — "quanti dipendenti partecipano eventi aziendali charity case study"
06/11 — "comunicato stampa evento tech charity esempi italiani 2024 2025"
07/11 — "run of show template evento ibrido sport corporate"
10/11 — "social listening durante evento live tool italiano GDPR"
11/11 — "pickup stampa embargo italiano percentuali benchmark"
13/11 — "cosa NON fare in discorso di squadra pre-evento"  ← [da qui parte la sessione Claude del 16/11]
```

### Ultima settimana

```
17/11 — "sleep deprivation program director notte prima evento live strategie"
18/11 — "cena di squadra pre-evento pro e contro"
19/11 — "cosa dire a CEO prima di un evento a rischio"
19/11 — "fiera di roma padiglione 6 planimetria evacuazione"
20/11 — "preghiera laica pre-performance"  ← [nessuno lo sa, è una sua cosa personale]
```

---

## 🤖 Luca Ferraresi — Robotics Program Lead

**Pattern**: query tecniche, inglese, brevi e dirette. Molte ricerche su GitHub e arXiv, non solo Google.

### Query significative

```
22/10 — [Google]     "Booster K1 knee joint backlash tolerance repair"
22/10 — [GitHub]     "booster-t1 ROS2 referee box client"
23/10 — [arXiv]      "humanoid bipedal fall recovery 2024 2025 benchmark"
25/10 — [Google]     "WiFi 6E dedicated network humanoid robot autonomous latency"
27/10 — [GitHub]     "rcll league referee client throttling"
29/10 — [Google]     "battery swap humanoid robot time optimization lipo pouch"
29/10 — [Stack Overflow]  "nvidia jetson orin hot swap live deployment"
01/11 — [Google Scholar]  "shadow gradient localization stereo RGB humanoid"
02/11 — [GitHub]     "b-human team code release 2025 localization patch"
05/11 — [Perplexity] "what is the acceptable rate of falls per match in RoboCup humanoid league 2025"
09/11 — [arXiv]      "reward shaping goal policy humanoid soccer threshold tuning"
10/11 — [GitHub]     "booster-robotics booster-sdk throttling referee signal bug"  ← [notte del bug]
12/11 — [Google]     "lipo pouch battery heating pre-match performance"
14/11 — [Google]     "RF interference 5GHz fair ottica Italia normativa"
17/11 — [Google]     "calibrazione finale humanoid vision giorno evento checklist"
19/11 — [GitHub]     "[il suo repo] — verifica ultimo commit tag v2.1"
20/11 — [Google]     "notte prima evento tecnico consigli di ingegnere senior"
```

---

## 🏥 Barbara Russo — Safety & Medical Lead

**Pattern**: molta Archivio Nereo (RAG aziendale) per policy interne + normativa italiana. Poche ricerche open web.

### Su Archivio Nereo (RAG interno)

```
23/10 — "DVR evento aziendale esterno + minori in platea template precedente"
           → restituisce: 3 DVR passati (Open Day, Family Day 2023, hackathon), nessuno perfettamente analogo
25/10 — "procedura operativa e-stop eventi aziendali con macchine mobili"
           → restituisce: 0 risultati rilevanti. Lacuna nota del RAG.
28/10 — "defibrillatore AED noleggio vs acquisto policy aziendale"
           → restituisce: policy 2023, acquisto consigliato sopra 3 utilizzi/anno
03/11 — "liberatoria minorenne ripresa video template azienda"
           → restituisce: 2 template, uno aggiornato GDPR 2024, usabile
06/11 — "RSPP contratto esterno evento massimale responsabilità"
           → restituisce: norme interne + esempio contratto 2025
11/11 — "checklist pre-evento safety 3 giorni prima"
           → restituisce: nulla di rilevante, lacuna. Barbara la crea ex novo.
14/11 — "gestione presenza istituzionale on. Gabrielli protocollo"
           → restituisce: procedura generica visite istituzionali, non 100% applicabile
```

### Su Google / Perplexity

```
29/10 — "[Google] evento fiera roma padiglione 6 piano evacuazione pubblico"
02/11 — "[Perplexity] quanti decibel tollera bambino 14-17 anni evento sportivo"
06/11 — "[Google] tecar polpaccio stiramento tempo recupero 40 anni"
11/11 — "[Perplexity] checklist safety officer evento sportivo-tech autonomi"
12/11 — "[Perplexity] decibel pubblico evento corporate 2000 persone rischi"
```

### Nota Barbara
> "Archivio Nereo funziona bene se quello che cerchi l'abbiamo già fatto prima. Per questo evento, il 40% delle cose non era mai stata fatta in azienda. Ho dovuto costruire nuovi documenti da zero e caricarli nel RAG. Ho sentito di aver fatto sistema oltre al singolo evento."

---

## 📣 Tommaso Marchi — Comms Lead

**Pattern**: Perplexity per ricerca contestuale + stampa, Google per fact-checking nomi/ruoli, uso pesante di Archivio Nereo per comunicazioni passate.

### Ricerche di context per press

```
23/10 — [Perplexity]  "casi studio evento robot charity Italia 2020-2025 copertura stampa"
25/10 — [Google]      "Milena Gabanelli Corriere Innovazione pezzi robotica ultimi 12 mesi"
26/10 — [Google]      "Riccardo Luna Repubblica coperture tech-sociale"
26/10 — [Google]      "Luca De Biase Sole 24 Ore posizione AI umanoide recente"
02/11 — [Perplexity]  "come reagiscono i giornalisti italiani alla narrativa robot autonomi in eventi corporate 2024 2025"
04/11 — [Perplexity]  "case study comunicazione crisi evento robotico fallimento"
05/11 — [Perplexity]  "crisis statement italiano tono esempi chirurgici aziende 2024"
08/11 — [Google]      "Fondazione Prometeo STEM Italia pickup stampa precedenti"
09/11 — [Google]      "on. Roberto Gabrielli Presidente Fondazione Prometeo background politico"
11/11 — [Archivio]    "dichiarazioni pubbliche Marco Bellini ultimi 24 mesi"
                       → sblocca: scoperta che Bellini 18 mesi fa ha detto qualcosa in contrasto con la narrativa oggi. Nessun giornalista l'ha rispolverato, ma Tommaso lo tiene presente.
13/11 — [Google]      "Giulia Bertagnolli cachet evento privato tecnologico"
16/11 — [Perplexity]  "pickup stampa 47 articoli benchmark evento corporate charity"
```

### Ricerche per scrivere bene

```
17/11 — [Perplexity]  "italiano giornalistico sobrio evitare frasi fatte charity"
18/11 — [Google]      "'siamo orgogliosi di' Google News occorrenze ultimi 30 giorni"
                       → motivazione: vuole contare quanto è abusato il cliché. Risultato: tanto. Lo evita.
19/11 — [Perplexity]  "closing statement italiano dopo evento charity esempi"
```

---

## ❤️ Elena Moretti — Charity & Partners Lead

**Pattern**: molta attenzione al linguaggio della solidarietà. Ricerche su casi italiani e UK.

```
23/10 — [Perplexity]  "parole da evitare in comunicazione charity italiana 2024 2025"
25/10 — [Google]      "Fondazione Prometeo bilancio 2024 2025 rendicontazione"
28/10 — [Google]      "ragazzi eventi pubblici protocolli etici coinvolgimento non esposizione"
02/11 — [Perplexity]  "consegna simbolica assegno evento corporate Italia come funziona"
04/11 — [Archivio]    "partnership precedenti fondazioni aziendali tracciatura MoU"
                       → restituisce: 11 MoU passati, 3 simili, nessuno con presenza istituzionale on evento pubblico
07/11 — [Perplexity]  "intervento testa istituzione evento STEM tono italiano 3 minuti"
08/11 — [Google]      "come scrivere breve discorso di ringraziamento evento aziendale"
13/11 — [Perplexity]  "90 secondi testo palco evento charity linguaggio non retorico"
14/11 — [Perplexity]  "gift matching double down donation evento live modelli"
18/11 — [Google]      "Codice Aperto STEM underserved ragazzi pickup stampa"
```

---

## 🎬 Alessandro Conti — Event Production Lead

**Pattern**: ricerca su casi internazionali (Webby, Slush, Red Bull). Poco Perplexity, molto YouTube + blog specializzati.

```
22/10 — [YouTube]     "Slush 2024 opening stage design breakdown"
23/10 — [blog]        "eventdesignlab Red Bull sport tech hybrid best practices"
27/10 — [Google]      "halftime segment 15 minutes corporate event pacing"
02/11 — [YouTube]     "WebSummit 2024 charity moment donation ceremony"
05/11 — [Google]      "ancora bolle live event Italia fornitori"
07/11 — [blog]        "live event production checklist 72 hours before"
14/11 — [YouTube]     "robot presentation corporate venue lighting tips"
17/11 — [Google]      "Fiera di Roma padiglione 6 planimetria standard tecniche"
19/11 — [Google]      "walkthrough finale evento ibrido scaletta"
```

---

## 🛰️ Stefano Bianchi — Technical Director

**Pattern**: molte ricerche hardware-specific + spec sheet. Utilizza forum specialistici (AVSForum, Broadcast.bz, H.264 community).

```
22/10 — [Google]       "Arri SkyPanel S60-C shadow fill lighting soccer sport"
23/10 — [spec site]    "broadcast camera 50fps flicker LED 5000K compatibility"
25/10 — [AV forum]     "[post tecnico sul canale 149 interference RoboCup Germany]"
29/10 — [Google]       "humanoid robot RGB stereo vision shadow calibration"
30/10 — [YouTube]      "lighting 20x12 indoor soccer pitch broadcast setup"
31/10 — [Perplexity]   "numero proiettori LED 300W 20x12m saturazione ombre vision robotica"
                        → dato usato per call con Massimiliano
02/11 — [Broadcast.bz] "replay server NewTek 3Play stability issues 2025"
05/11 — [Google]       "WiFi 6E enterprise AP dedicato canale 149 settings"
08/11 — [Reddit]       "ubiquiti vs cisco meraki large venue event temporary"
11/11 — [Google]       "[vendor specifico] ordine urgente spedizione Italia 72h"
14/11 — [AV forum]     "padiglione fiera Roma cablaggio CAT6A predisposto"
17/11 — [Google]       "RF survey strumento professionale Italia rental"
19/11 — [Google]       "backup power generator silent venue corporate no noise"
```

---

## 👥 Giulia Peretti — Human Squad Lead

```
23/10 — [Archivio]  "visita medica sportiva non agonistica policy aziendale"
26/10 — [Archivio]  "liberatoria dipendente attività extra-lavorativa azienda"
29/10 — [Google]    "preparatore atletico freelance Roma dipendenti casual calcetto"
03/11 — [Perplexity] "selezione roster aziendale equo inclusivo criteri"
08/11 — [Google]    "stiramento polpaccio tempi ritorno amateur 40 anni"
14/11 — [Perplexity] "motivational pep talk coach team amateurs evento pubblico"
17/11 — [Google]    "divisa calcetto aziendale produzione veloce 5 giorni Italia"
```

---

## ⚖️ Valeria De Santis — Legal & Finance

**Pattern**: Valeria usa pochissimo LLM ma molta ricerca su database legali specializzati (Leggi d'Italia, Wolters Kluwer, Eur-Lex).

```
23/10 — [Leggi d'Italia] "D.Lgs 81/08 eventi corporate robot automi responsabilità"
25/10 — [WK Cedam]       "assicurazione RC evento pubblico robotica precedenti"
29/10 — [Archivio]       "contratti fornitori broadcast ultimi 24 mesi modelli"
02/11 — [Leggi d'Italia] "minorenni presenza evento corporate liberatoria GDPR interazione"
06/11 — [Archivio]       "partnership università ricerca MoU template IP pubblicazione"
09/11 — [Leggi d'Italia] "trasporto robot import Cina dazio IVA gestione"
12/11 — [Archivio]       "crisis statement media approvazione flusso precedenti"
16/11 — [Google]         "polizza onnicomprensiva evento 2000 capienza massimali Italia"
18/11 — [Archivio]       "contratto commentatrice freelance evento live diritti immagine"
```

---

## 📐 Chiara Volpe — Content Producer

```
23/10 — [Pinterest]   "corporate charity event key visual 2024 2025"
25/10 — [Behance]     "robot soccer event branding"
28/10 — [Google]      "video teaser evento robotico charity Italia esempi"
02/11 — [Perplexity]  "social playbook evento live 30 post template piattaforme"
05/11 — [Dribbble]    "live event graphic package sport esports scoreboard overlay"
08/11 — [Google]      "reel formato Instagram 9:16 tempi massimi retention 2025"
13/11 — [YouTube]     "TikTok clip backstage corporate event tone of voice"
15/11 — [Google]      "LinkedIn algorithm 2026 long form vs video"
17/11 — [Behance]     "pin souvenir evento tech design esempi"
19/11 — [Canva]       "caption template Instagram reel bilingual it/en"
```

---

## 🎙️ Andrea Moro — Broadcast Director

```
22/10 — [Broadcast.bz]  "humanoid robot POV cam mount lightweight 95cm"
25/10 — [Google]        "6 camera live event small pitch crew minimal"
29/10 — [Google]        "slow motion 120fps live event clip instant replay"
02/11 — [Forum]         "NewTek Tricaster TC2 Elite workflow corporate 6 camera"
05/11 — [Google]        "robot POV camera attachment GoPro vs DJI Osmo weight"
09/11 — [YouTube]       "Phantom vs 120fps consumer real-time pipeline"
12/11 — [Google]        "cartello grafico 'technical pause' broadcast italiano sport"
17/11 — [Broadcast.bz]  "replay server NewTek 3Play restart random troubleshooting 2025"
19/11 — [forum]         "broadcast crew call time sabato 21 novembre 2026 Roma logistica"
```

---

## 🤖 Vincenzo Suriani (SPQR)

**Pattern**: Vincenzo è un ricercatore, non un manager. Cerca paper e repository, non template.

```
23/10 — [arXiv]         "humanoid soccer localization shadow gradient compensation 2025"
25/10 — [GitHub]        "b-human-2024 localization branch"
27/10 — [Google Scholar] "referee signal throttling ROS2 humanoid"
29/10 — [arXiv]         "reward shaping goalie policy autonomous soccer"
05/11 — [GitHub]        "[codice privato SPQR — verifica tag]"
08/11 — [Google]        "RoboCup HSL 2026 rules update after october"
10/11 — [GitHub]        "[il suo repo] bug report referee double reset"  ← [notte del fix]
14/11 — [arXiv]         "explainable AI demo context public event narrative"
17/11 — [Google]        "come spiegare 5v5 autonomo al grande pubblico tecniche"
```

---

## Pattern trasversali osservati

### 1. **Volume**
Picchi di ricerca:
- Settimana DR2 (27-31 ottobre) → volume 3x il normale
- Settimana annuncio stampa (9-13 novembre) → volume 2x
- Ultima settimana (17-20 novembre) → volume in discesa. Il team è più nelle conversazioni umane che nelle ricerche.

### 2. **Shift nell'uso degli strumenti**
Nella fase iniziale del periodo si fa molta ricerca Google tradizionale. Verso la fine, chi ha integrato Perplexity lo usa per le ricerche più complesse. **Archivio Nereo cresce in uso** man mano che il team identifica pattern interni utili. Tre Lead (Barbara, Valeria, Elena) dichiarano di aver "capito come si usa" proprio in questo evento, per stress funzionale.

### 3. **Query "meta" sul processo**
Emergono ricerche non sul cosa fare ma sul come stare dentro al momento:
- "cosa NON dire in discorso pre-evento"
- "come gestire 30 giorni prima di un evento critico"
- "sleep deprivation evento live strategie"

Questo indica un team che usa le ricerche web anche come strumento di auto-riflessione, non solo operativa.

### 4. **Gap nel RAG aziendale**
Sono emersi 7 "buchi" nel RAG interno, dove nessun documento passato copriva il caso specifico. Per ciascuno, il Lead ha creato nuovo materiale che è stato re-ingerito. Il RAG aziendale al termine del periodo è **sensibilmente più ricco** di quanto fosse a inizio periodo — un side-effect prezioso dell'evento.

### 5. **Privacy e GDPR**
Valeria ha regolarmente spinto perché le ricerche "delicate" (es. dati Fondazione, informazioni on. Gabrielli) avvenissero su strumenti certificati (Perplexity Enterprise, Archivio Nereo) e non su ChatGPT consumer. Questo ha **prevenuto almeno 2 casi** potenziali di data leak (uno identificato, uno ipotetico).

### 6. **Ciò che NESSUNO ha cercato**
Alcune ricerche che ci saremmo aspettati, e che invece non ci sono:
- "cosa fare se robot ferisce spettatore" → Barbara si è rifiutata di cercarlo su motori pubblici. Ha chiamato il broker.
- "costo vero evento simile" → nessuno ha cercato benchmark esterni. Si sono fidati della loro costruzione dal basso.
- "come ottenere copertura TV" → non è stata una priorità. È arrivata spontaneamente.

### 7. **Pattern settimanale**
- Lunedì mattina: picchi di query di "status & aggiornamento"
- Mercoledì: picchi di query operative ("come fare X")
- Venerdì pomeriggio: query di "chiusura settimana" e preparazione weekend
- Weekend: silenzio quasi completo tranne per Luca e Vincenzo (coding)

---

## Totale stimato ricerche nel periodo per Lead

| Lead | Ricerche stimate | Strumenti principali |
|---|---|---|
| Federica | ~180 | Perplexity, Google |
| Luca | ~260 | Google, GitHub, arXiv, Stack Overflow |
| Tommaso | ~140 | Perplexity, Google, Archivio Nereo |
| Chiara | ~120 | Pinterest, Behance, Dribbble, Google |
| Stefano | ~210 | Google, forum tecnici, spec sheet |
| Vincenzo | ~180 | GitHub, arXiv, Google Scholar |
| Andrea | ~90 | Broadcast forums, YouTube |
| Barbara | ~75 | Archivio Nereo, Leggi d'Italia |
| Elena | ~55 | Perplexity, Archivio |
| Valeria | ~80 | Leggi d'Italia, WK, Archivio |
| Alessandro | ~60 | YouTube, blog specializzati |
| Giulia | ~45 | Perplexity, Archivio |
| **Totale** | **~1.495** | |
