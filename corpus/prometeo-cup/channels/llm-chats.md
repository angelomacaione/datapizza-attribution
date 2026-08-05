# llm-chats.md
**Periodo**: T-1 mese → T-1 giorno (21 ottobre → 20 novembre 2026)
**Strumenti usati dal team**:
- **Claude** (uso interno azienda via abbonamento enterprise) — Federica, Luca, Barbara, Elena, Tommaso
- **ChatGPT** (account personali) — Alessandro, Chiara, Andrea (broadcast), Vincenzo
- **Perplexity** (ricerche rapide) — tutti, trasversale
- **GitHub Copilot** — Luca, SPQR team
- **Grammarly + DeepL** — Tommaso, Elena (inglese)

**Volume stimato**: oltre 600 conversazioni LLM nel periodo, da micro-query (10 sec) a sessioni lunghe (90 min).

Quello che segue è una **selezione curata** di sessioni significative, un estratto per Lead, in cui l'LLM è stato usato come **pensatoio**, non come search engine.

---

## 🎯 Federica Mazzarese — Program Director

### Sessione 1 — Claude, 24 ottobre 2026, 06:22 (prima del kickoff giornata)

**Contesto**: la sera prima DR2 pre-brief, Federica non dorme bene. Apre Claude su mobile.

> **Federica**: Sei un coach esperto in gestione di program director sotto pressione. Sto preparando un evento live con robot autonomi vs dipendenti per beneficenza, tra 27 giorni, budget ~600k, team di 75 persone. Oggi abbiamo il pre-briefing del dry run 2. Ho la sensazione che 2 Lead abbiano paura ma non lo stiano dicendo. Come faccio a creare lo spazio perché parlino SENZA forzarli a esporsi?

*[Risposta dell'LLM: struttura di "3 inviti progressivi" + esempi di frasi-ponte che abbassano il rischio percepito di ammettere dubbi. Riferimento al concetto di psychological safety di Amy Edmondson.]*

> **Federica**: Mi piace l'idea delle frasi-ponte. Fammi 5 esempi in italiano naturale, non calcati sull'inglese.
>
> **Federica**: [dopo risposta] Il terzo, "Io per prima una cosa che non mi torna è...", è perfetto. Uso quello. Grazie.

**Nota**: Federica userà quella frase effettivamente nella stand-up del 28, e Barbara sbloccherà l'issue del defibrillatore.

---

### Sessione 2 — Claude, 1 novembre 2026, 22:40

**Contesto**: dopo il DR2, delta budget luci in arrivo. Federica sta preparando la telefonata al CFO.

> **Federica**: Devo chiamare domani il CFO per un delta budget di 28k su un progetto da 620k. Contingency scende dal 72% al 54%. Ho già 3 pallina in fila con lui, non è arrabbiato ma è di carattere preciso e le sorprese le vive male. Aiutami a strutturare la call in 4 punti max. Deve durare 15-20 minuti.

*[Risposta LLM: struttura "anchor → fact → options → decision" con time-boxing per ciascuno.]*

> **Federica**: Ok ma voglio evitare di sembrare in ansia. Se mi vede insicura, lui si preoccupa. Suggerimenti di linguaggio corporeo/voce?
>
> *[L'LLM propone: respirazione pre-call 4-4-6, apertura con fatto neutro non emozionale, evitare parole come "problema/urgente/critico", sostituire con "delta/aggiornamento/decisione aperta".]*
>
> **Federica**: Perfetto. Preparo anche il seguito: se mi dice "no", cosa faccio?

**Nota**: la call si terrà il 1° nov alle 16:00, durata 22 min, esito positivo.

---

### Sessione 3 — Claude, 16 novembre 2026, 00:14

**Contesto**: Federica ha 5 giorni all'evento. Scrivendo il discorso dell'all-hands finale.

> **Federica**: Ti sto per condividere la bozza del mio discorso di venerdì sera all'all-hands pre-evento. È davanti a 38 persone della mia squadra core dopo 7 mesi di lavoro insieme. L'evento è domenica dopo. Non voglio essere retorica e non voglio piagnucolare. Voglio essere vera e utile. Ecco la bozza: [testo]. Feedback?

*[L'LLM risponde con feedback sezione per sezione, segnala 2 passaggi che scivolano nell'enfatico, suggerisce un rafforzativo sulla parte "cosa può andare male".]*

> **Federica**: Hai ragione sull'enfatico. Riscrivo senza "sogno", senza "storia", senza "impresa". Solo fatti ed emozione quando serve davvero.
>
> **Federica**: [dopo 2 iterazioni] Grazie. È pronto. Per domani.

**Nota**: il discorso finale è quello documentato in `remote-meetings.md` punto 8.

---

## 🤖 Luca Ferraresi — Robotics Program Lead

### Sessione 1 — Claude, 29 ottobre 2026, 08:11

**Contesto**: mattina di DR2. Luca sta caricando sul muletto hardware backup.

> **Luca**: Ho un K1 autonomo che in DR2 deve eseguire 3 match da 20 min ciascuno. Temperatura ambiente 19°C padiglione fieristico. Motori sintered NdFeB PMSM, profilo uso 60% walking + 20% running + 20% standing. Dammi stima realistica battery degradation e protocollo swap ottimale per garantire continuità senza downtime > 15 secondi.

*[Risposta LLM tecnica con calcolo approssimativo cicli e raccomandazione di pre-heating batterie spare.]*

> **Luca**: Mi hai convinto sul pre-heating. Domanda secondaria: se passiamo a WiFi 6E 5GHz esclusivo come consigliato, la latenza end-to-end robot→referee box scende a quanto? Target 80ms.

*[LLM dà stima e propone 3 fattori di rischio che potrebbero far salire la latenza.]*

> **Luca**: Il terzo fattore (interferenza cross-channel da AP vicini) è esattamente quello che abbiamo nel padiglione 7 accanto. Bingo. Attivo discussione con Stefano.

---

### Sessione 2 — ChatGPT (suggerito da Vincenzo per velocità), 10 novembre 2026, 02:15

**Contesto**: Vincenzo ha trovato il bug notturno. Luca sta verificando l'impatto della patch.

> **Luca**: Given a ROS2 Humble autonomous humanoid soccer stack, if I add a client-side throttling (3 lines of code) on referee signal processing to prevent double-reset on rapid foul sequences, what are the failure modes I should test for in <6 hours before greenlighting a new tag? Context: production deploy in <12 days.

*[ChatGPT risponde con checklist 9 test: race conditions, throttle timing, referee queue overflow, behavior under real-time jitter, etc.]*

> **Luca**: Test 4 (jitter) non l'avevamo in piano. Grazie. Aggiungo stamattina.

---

## 📣 Tommaso Marchi — Comms Lead

### Sessione 1 — Claude, 5 novembre 2026, 11:30

**Contesto**: drafting dei 3 crisis statement pre-approvati.

> **Tommaso**: Ti chiedo di aiutarmi a scrivere 3 dichiarazioni di crisi pre-approvate per un evento corporate con robot autonomi + dipendenti + bambini in platea + Presidente Fondazione onlus. Scenari: (A) infortunio lieve a dipendente, (B) rottura grave di un robot durante la partita live, (C) blackout rete che interrompe il gioco per >5 min. Voglio: tono italiano sobrio, 80-120 parole ciascuna, niente "in linea con le procedure", niente "le nostre scuse ai", niente PR-speak. Solo umano e credibile.

*[L'LLM produce 3 bozze.]*

> **Tommaso**: Lo scenario A è buono. Scenario B ha un problema: dici "la tecnologia è ancora giovane" e sembra difensiva. Toglilo. Riscrivi.
>
> **Tommaso**: [dopo 4 iterazioni] Perfetto. Rivedo con Legal domani.

**Nota**: le dichiarazioni non verranno mai usate (nessun incidente grave), ma il file circolerà in email Thread #33 e costruirà fiducia nel management.

---

### Sessione 2 — Claude, 9 novembre 2026, 16:47

**Contesto**: Tommaso sta preparando i talking points per Bellini.

> **Tommaso**: Il CHRO sponsor dovrà rispondere a domande di giornalisti la sera prima dell'evento. La domanda più difficile che gli faranno è: "Perché non avete semplicemente donato i 600 mila euro direttamente alla fondazione?" Aiutami a costruire una risposta in 80 parole, con 3 punti solidi, che:
> - non sia difensiva
> - non svaluti la donazione pura
> - mostri che avete pensato a questa obiezione
> - lasci l'ascoltatore pensando che l'evento è la scelta giusta, non che sia una giustificazione

*[L'LLM propone risposta in 3 iterazioni progressive, Tommaso chiede di aggiungere la parte "la meno raccontabile ma è vera" come tratto di trasparenza.]*

**Nota**: Bellini userà questa risposta quasi parola per parola con Gabanelli il 10 novembre.

---

## 🏥 Barbara Russo — Safety & Medical Lead

### Sessione 1 — Claude, 11 novembre 2026, 20:30

**Contesto**: Barbara sta finalizzando il DVR evento.

> **Barbara**: Sono RSPP di un evento corporate in venue fieristico 2000 capienza, con 10 robot autonomi 20kg, 16 giocatori umani in campo, 8 minorenni in platea riservata, 3 VIP istituzionali, durata match 2x10 min + cerimonie. Devo produrre una checklist di controlli pre-match da eseguire nelle 4 ore precedenti il calcio d'inizio. Voglio: ordine cronologico stretto, ownership chiara per ciascun item, no overlap con controlli già fatti nel walkthrough del giorno prima. Target 20-25 item max.

*[L'LLM genera checklist cronologica 23 item da T-240 min a T-0, con ownership per ciascuno.]*

> **Barbara**: 19 va modificato: l'ambulanza non deve "essere in posizione alle 14:30" ma "confermare canale radio operativo entro 14:30". Cambia.
>
> **Barbara**: Mi serve anche un "fail checklist": se ALMENO UNA di queste è red, non si inizia. Quali sono? Te ne segnalo max 5.

*[L'LLM propone 5 criteri di blocker assoluto. Barbara li accetta con modifica 1.]*

**Nota**: questa checklist diventa il documento più stampato dell'evento, appeso a 3 postazioni fisiche il giorno.

---

## ❤️ Elena Moretti — Charity & Partners Lead

### Sessione 1 — Claude, 13 novembre 2026, 18:15

**Contesto**: Elena sta scrivendo il pitch che verrà letto sul palco da CEO e Presidente Fondazione durante la consegna simbolica.

> **Elena**: Scrivi un testo di 90 secondi di lettura per una consegna simbolica di assegno a fine evento. Lo legge il CEO aziendale e lo completa il Presidente della Fondazione beneficiaria. Contesto: Fondazione Prometeo fa alfabetizzazione STEM per ragazzi di contesti fragili. Il programma si chiama "Codice Aperto". Voglio:
> - pubblico di 2000 in venue + broadcast
> - niente retorica da evento benefico
> - un fatto concreto sulla Fondazione (es. quante ore di corso garantisce la donazione)
> - una dedica finale ai 8 ragazzi presenti in platea, senza nominarli per non creare disagio
> - ritmo leggibile ad alta voce, pause segnalate con /

*[L'LLM produce bozza. Elena la riscrive 3 volte, spostando la parte sui ragazzi all'inizio invece che alla fine.]*

> **Elena**: Ultimo. "Un pensiero speciale va" in italiano è brutto. Come lo dico altrimenti?

*[L'LLM propone 5 alternative. Elena sceglie "Abbiamo portato qui stasera anche loro" con tono diretto.]*

---

## 🎬 Alessandro Conti — Event Production Lead

### Sessione 1 — ChatGPT, 28 ottobre 2026, 23:04

**Contesto**: Alessandro sta disegnando il ritmo della scaletta.

> **Alessandro**: I'm designing the flow for a live 2-hour corporate-charity hybrid event: 30 min pre-show + 10 min opening + 2x10 min match with halftime + 15 min halftime entertainment + 20 min post-match ceremony. The audience is 2000 people, mix corporate employees, VIPs, kids. The match itself is autonomous robots vs humans (robots will lose visibly). I need to structure the halftime entertainment (15 min) to maintain energy WITHOUT competing with the emotional peak of the charity donation. What's the arc?

*[ChatGPT propone struttura in 3 atti con variazione ritmica.]*

> **Alessandro**: The second act is too loud. I want halftime to be a moment of breath, not another peak. Rewrite.

*[Itera 3 volte finché Alessandro arriva alla struttura: (a) warm-down atletico 4 min, (b) intervento tecnico Vincenzo 6 min, (c) pre-warming emozione finale 5 min.]*

---

## 🛰️ Stefano Bianchi — Technical Director

### Sessione 1 — Claude, 31 ottobre 2026, 09:00 (durante DR2 debrief)

**Contesto**: dopo la scoperta delle ombre sulle travi. Sta contattando Massimiliano di Luce Eventi.

> **Stefano**: Dammi una stima rapida: per un campo 20x12m, robot con camera RGB stereo altezza 90cm, devo garantire illuminazione che NON produca shadow gradient sul piano di gioco. Luci esistenti: LED 280W 5000K appesi a 9m, 14 unità. Ho scoperto che le travi strutturali proiettano ombre longitudinali. Opzioni: (A) aggiungere proiettori di riempimento, (B) cambiare temperatura colore per ridurre contrasto, (C) rivestimento selettivo pavimento. Confronto lampo?

*[L'LLM analizza pro/contro. Consiglia A con specifiche tecniche.]*

> **Stefano**: Quanti proiettori e di che potenza per saturare le ombre nei settori centrali senza andare in over-exposure sulle camere broadcast?

*[LLM calcola con stima 10-14 proiettori 300W.]*

**Nota**: Stefano arriva alla call con Massimiliano con numeri precisi. Massimiliano capisce che Stefano sa di cosa parla e non tenta di gonfiare il preventivo.

---

## 📐 Chiara Volpe — Content Producer

### Sessione 1 — Claude, 6 novembre 2026, 15:30

**Contesto**: sta pianificando il piano contenuti giorno dell'evento.

> **Chiara**: Mi serve la scaletta contenuti social di un evento corporate-charity live. Canali: Instagram (reels + stories), LinkedIn (post long-form), X/Twitter (live thread), TikTok (reel finali). Durata evento: 14:00-17:30. Voglio 30 post totali distribuiti. Ho un team di 3 persone (una per piattaforma + me che curo). Dammi template + distribuzione temporale.

*[L'LLM propone piano 30 post + matrice.]*

> **Chiara**: Non mi convincono i 9 su X. Li riduciamo a 5, lo spazio lo sposto su LinkedIn che è dove la nostra audience tecnica è più densa.

*[Rivede.]*

> **Chiara**: Ok. Ora dammi 10 caption "ready to copy" per le reaction più probabili: (1) gol dei dipendenti, (2) robot che cade, (3) esultanza, (4) momento commozione Fondazione, (5) assegno consegnato, (6) fischio finale. Tono: sobrio ma caldo. No emoji a caso.

---

## 🎙️ Andrea Moro — Broadcast Director

### Sessione — ChatGPT, 12 novembre 2026, 20:40

**Contesto**: piano camera per il match.

> **Andrea**: I'm directing a 6-camera shoot for an autonomous robot vs human soccer match, 10 robots field-side (small, 95cm tall). I need dynamic coverage without losing the "robots are the protagonist" feel. Cam 1-2 fixed wide, Cam 3 mid-side tracking, Cam 4 robot-POV (mounted on robot head), Cam 5 handheld near pit, Cam 6 reverse angle for human players reactions. Is this setup solid? What am I missing?

*[ChatGPT propone di aggiungere una slow-motion camera a 120fps per catch-moments e una drone cam indoor per overhead shot.]*

> **Andrea**: We can't do drone indoor (safety constraint). But the 120fps slow-mo we have in budget. Adding it.

---

## 📚 Vincenzo Suriani (SPQR, guest)

### Sessione — Claude, 25 ottobre 2026, 23:50 (bilingue, misto IT/EN)

> **Vincenzo**: Ho un dubbio meta. Il nostro team universitario ha rilasciato codice per RoboCup ogni anno da 8 anni. Questa volta lo rilascio in un evento commerciale sponsorizzato da una grossa azienda. Mi preoccupa il messaggio che questo manda alla comunità scientifica. Come mi pongo?

*[L'LLM propone 3 framing diversi, uno dei quali: "presentarsi come portatore di conoscenza aperta IN un contesto commerciale, non come fornitore AL contesto commerciale"]*

> **Vincenzo**: Questo secondo framing è quello giusto. Lo userò nel mio intervento di halftime. Grazie.

**Nota**: Vincenzo userà esattamente questa distinzione nel suo 6-minute intervento live di halftime. Pubblico in sala particolarmente colpito.

---

## 🔍 Note su come il team ha usato gli LLM

Emergono 5 pattern:

### 1. LLM come **spin partner**, non come enciclopedia
Nessuno dei Lead ha usato l'LLM come "Google migliore". Tutti (anche i meno tecnici) hanno chiesto feedback su draft, domande difficili, strutturazioni di decisione. L'output è sempre stato rielaborato, non copiato.

### 2. **Differenza generazionale e culturale**
- Federica, Tommaso, Elena → Claude come coach, dialoghi lunghi in italiano
- Luca, Stefano, Andrea → ChatGPT per tecnica, in inglese, query brevi
- Chiara → Claude per scrittura, ChatGPT per brainstorming
- Alessandro → ChatGPT occasionale, preferisce pensare scrivendo su carta
- Barbara → Claude solo per checklist, per tutto il resto preferisce umani
- Valeria (Legal) → quasi zero uso LLM. Fiducia bassa, privacy concern alto, "non è il mio strumento"

### 3. **Orari d'uso**
Picchi di uso LLM:
- **Notti/mattina presto** (05:30-08:00): quando la testa è lucida ma il team dorme
- **Fine pomeriggio** (17:30-19:30): pre-chiusura giornata, preparazione per il giorno dopo
- **Notti tarde** (23:00-02:00): solo per emergenze o quando si è bloccati

### 4. **Uso "terapeutico"**
Vincenzo e Federica hanno usato più volte l'LLM per **chiarirsi le idee prima di una conversazione umana importante**. Non per la risposta, per il pensiero lungo. "Scrivere a qualcuno che ti ascolta pazientemente aiuta a capire cosa vuoi davvero dire."

### 5. **Limiti rispettati**
Nessuno dei Lead ha usato LLM per:
- decisioni legali vincolanti (Valeria)
- diagnosi mediche (Barbara)
- decisioni sulla sicurezza hardware (Luca)
- drafting di email a giornalisti (Tommaso — "troppo rischio di suonare generico")
- momenti emotivi con colleghi (tutti: "per quello c'è la voce")

L'LLM è stato usato come **strumento cognitivo**, non come decisore. La decisione è sempre rimasta in capo alle persone.

---

## Metrica finale periodo

| Lead | Sessioni LLM stimate | Durata totale stimata |
|---|---|---|
| Federica | ~85 | ~12h |
| Luca | ~110 (molte tecniche brevi) | ~8h |
| Tommaso | ~65 | ~10h |
| Chiara | ~55 | ~7h |
| Barbara | ~20 | ~3h |
| Elena | ~25 | ~4h |
| Stefano | ~40 | ~4h |
| Andrea | ~30 | ~3h |
| Alessandro | ~15 | ~2h |
| Vincenzo (ospite) | ~18 | ~2h |
| Valeria | ~3 | ~20 min |

Totale team: ~450-500 sessioni LLM / ~55 ore / 30 giorni.
Costo economico diretto: trascurabile (enterprise plans).
Valore: difficile da misurare, ma plausibilmente 100+ ore di "pensiero aggiuntivo" che altrimenti sarebbero state rinviate o saltate.
