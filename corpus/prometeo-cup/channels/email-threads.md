# email-threads.md
**Periodo**: T-1 mese → T-1 giorno (21 ottobre → 20 novembre 2026)
**Canale**: Outlook / Exchange aziendale
**Totale thread nuovi aperti in questo periodo**: 23 — qui i 12 più rilevanti

---

## Cast ricorrente
- **Marco Bellini** — Executive Sponsor / CHRO
- **Federica Mazzarese** — Program Director (PD)
- **Luca Ferraresi** — Robotics Program Lead (interno)
- **Vincenzo Suriani** — SPQR Sapienza, Team Leader
- **Alessandro Conti** — Event Production Lead
- **Stefano Bianchi** — Technical Director
- **Barbara Russo** — Safety & Medical Lead
- **Elena Moretti** — Charity & Partners Lead
- **Tommaso Marchi** — Comms Lead
- **Valeria De Santis** — Legal & Finance Lead
- **Giulia Peretti** — Human Squad Lead
- **Chiara Volpe** — Content Producer
- **Andrea Moro** — Broadcast Director

---

## Thread #28 — "Hardware status post-repair + lista definitiva robot per DR2"
**Aperto**: 22 ott 2026, 09:14 · **Messaggi**: 14 · **Chiusura**: 24 ott 17:02
**Partecipanti**: Luca Ferraresi, Vincenzo Suriani, Federica Mazzarese, Valeria De Santis, Alessandro Conti

**Sintesi**: conferma rientro dei 2 K1 riparati, uno con ritardo di 4 giorni via DHL Express Shanghai. Confermato backup con 3 NAO prestati da SPQR. Si allinea la dotazione per DR2 a 11 robot (10 in campo + 1 spare), accettando di scendere da 12 previsti.

### Messaggi chiave

**[22 ott, 09:14] Luca Ferraresi → thread**
> Team, aggiornamento hardware:
>
> - K1-03 e K1-08 ripartiti da Shenzhen il 19/10, tracking DHL allegato.
> - ETA K1-03: 24/10 (sabato). ETA K1-08: 28/10 — *dopo il freeze DR2*.
> - Copertura backup: Vincenzo conferma 3 NAO della dotazione SPQR, disponibili dal 26/10.
>
> Proposta operativa: DR2 con 10 K1 + 1 NAO utilizzato come "8° giocatore simulato" nei drill di localization. Accettabile?

**[22 ott, 10:41] Vincenzo Suriani → thread**
> Confermo disponibilità NAO. Due richieste:
> 1. Trasporto a/r da Sapienza coperto da voi (già quotato €680 con assicurazione).
> 2. Codice sorgente del nostro porting K1→NAO rimane con noi (già nel MoU, solo per chiarezza).

**[22 ott, 14:08] Alessandro Conti → thread**
> Per produzione: 10 robot in campo + 1 spare è il minimo tecnico. Se perdiamo ancora anche solo 1 K1 prima del 21/11 abbiamo problema narrativo grosso. Si può chiedere a Booster uno shipment espresso spare direttamente da magazzino EU?

**[23 ott, 11:22] Valeria De Santis → Luca, Federica**
> Ho contattato Génération Robots (FR). Hanno 1 K1 demo disponibile a rental per 3 settimane, €4.200 + IVA + cauzione 50%. Se lo vogliamo va deciso entro venerdì 24.

**[24 ott, 16:47] Federica Mazzarese → thread (decisione)**
> OK al rental del K1 demo da GR. Valeria, procedi. Marco Bellini informato via DM.
> Copertura operativa confermata: 10 K1 + 1 K1 spare + 3 NAO backup + 2 NAO drill. Siamo good per DR2.

---

## Thread #29 — "DR2 — run of show tecnico + freeze del codice SPQR"
**Aperto**: 25 ott 2026, 08:03 · **Messaggi**: 22 · **Chiusura**: 30 ott 22:47
**Partecipanti**: Luca Ferraresi, Stefano Bianchi, Vincenzo Suriani, Alessandro Conti, Andrea Moro, Federica Mazzarese

**Sintesi**: programmazione tecnica del dry run #2 (giovedì 29 ottobre, Fiera di Roma Padiglione 6, 9:00-23:00). Freeze codice SPQR al 27 ottobre ore 18:00. Introdotto protocollo di rollback in caso di regressione.

### Messaggi chiave

**[25 ott, 08:03] Stefano Bianchi → thread**
> Allegato: `DR2-runbook-v3.xlsx`.
> Highlights:
> - 09:00 power-up completo padiglione
> - 09:30–11:00 calibrazione camere + white balance robot vision
> - 11:00–12:30 prova rete (separazione SSID robot / broadcast / pubblico)
> - 14:00–17:00 match simulato 2×10 min × 3 cicli
> - 17:30–19:00 scenari crisis (robot caduto grave, e-stop, infortunio)
> - 20:00 debrief tecnico
>
> Serve conferma Vincenzo su versione codice freezata.

**[26 ott, 19:34] Vincenzo Suriani → thread**
> Freeze su **tag `hsl-2026-dr2-v1`** su GitHub privato, push entro martedì 27 ore 18:00.
> Changelog rispetto a DR1:
> - fix localization su parquet lucido (ombre del proiettore)
> - nuova policy di ball approach: riduzione dello swerving (meno spettacolare ma più robusto)
> - soft e-stop remoto via referee box (richiesta di Barbara)
> - battery management: warning sonoro a 20% invece che 15%
>
> Nota: il fix locale ombre NON è stato testato con l'illuminazione finale del padiglione. Rischio residuo medio.

**[27 ott, 20:19] Luca Ferraresi → thread**
> Conferma tag pushato 18:47. Primo smoke test in laboratorio OK. Portiamo un Jetson di backup per hot-swap in caso di kernel panic (successo in DR1).

**[30 ott, 22:47] Alessandro Conti → thread (wrap DR2)**
> DR2 chiuso. 47 issue aperte, di cui 6 bloccanti, 14 alte, 27 medie/basse. Report dettagliato nel thread #32. Buona riuscita del match simulato (2 cicli su 3 completati senza interruzione). Grazie a tutti.

---

## Thread #30 — "🚨 Illuminazione padiglione — ombre longitudinali compromettono vision robot"
**Aperto**: 30 ott 2026, 23:58 (in fase DR2 debrief) · **Messaggi**: 41 · **Chiusura**: 4 nov 11:33
**Partecipanti**: Stefano Bianchi, Luca Ferraresi, Vincenzo Suriani, Federica Mazzarese, Alessandro Conti, fornitore lighting (Luce Eventi Srl — Massimiliano)

**Sintesi**: emerge durante DR2 che le travi del padiglione proiettano ombre longitudinali sul campo nei primi 10 minuti post-power-up. La vision dei K1 sbaglia stima della profondità nella fascia centrale. Richiesto intervento urgente del fornitore illuminotecnico.

### Messaggi chiave

**[30 ott, 23:58] Stefano Bianchi → thread (post-DR2)**
> Situazione:
>
> 📸 Analisi video DR2, 15° minuto del match 2:
> - 3 robot su 10 hanno perso tracking palla nei settori B3 e C3 (centrocampo lato ovest)
> - Causa: ombre lunghe dalle travi del padiglione, non presenti in sopralluogo settembre perché ci eravamo illusi sulla temperatura colore
> - Latitudine di errore profondità: fino a ±45 cm
>
> Serve ri-disegno luci. Non è un "aggiusta un faro", è un ridisegno zone 3 e 5.
>
> @Massimiliano (in cc): call domattina alle 9?

**[31 ott, 09:47] Massimiliano (Luce Eventi) → thread**
> Possibile. Due opzioni:
> **A)** 12 proiettori LED 300W aggiuntivi orientati sul piano (+€18.400 setup + €3.200/giorno)
> **B)** Pavimento in feltro nero opaco sulle zone critiche che assorbe gli spill (+€9.800 una tantum, 4 giorni lavoro)
>
> Opzione B più economica ma cambia l'estetica del campo (non più verde pieno). Opzione A è quella pulita ma ricarichi elettrici aumentano.

**[31 ott, 15:22] Luca Ferraresi → thread**
> Consultato Vincenzo: la policy di vision dei K1 è **addestrata su campo verde**. Cambiare a campo con settori neri comporta retraining di almeno 4 giorni. Non è nei tempi.
> Dobbiamo andare su opzione A.

**[1 nov, 10:08] Valeria De Santis → Federica, privato in cc**
> Delta di budget: circa €28k tra setup e 3 giorni evento. Abbiamo contingency al 72% — coprire qui significa eroderla al 48%. Ok a procedere?

**[1 nov, 12:44] Federica Mazzarese → thread**
> Go opzione A. Valeria conferma copertura. Massimiliano, ti serve firma ordine integrativo entro oggi per cantiere in tempo?

**[4 nov, 11:33] Stefano Bianchi → thread (chiusura)**
> Installati 12 proiettori ieri sera. Test vision stamattina con codice SPQR: errore profondità sceso a ±6 cm. Chiudo thread. Prossima verifica al walkthrough del 20/11.

---

## Thread #31 — "Richiesta Fondazione Prometeo — partecipazione live del Presidente + racconto bambini beneficiari"
**Aperto**: 2 nov 2026, 10:19 · **Messaggi**: 19 · **Chiusura**: 7 nov 18:05
**Partecipanti**: Elena Moretti, Federica Mazzarese, Tommaso Marchi, Marco Bellini, direttrice Fondazione (Silvia Tartaglia)

**Sintesi**: la Fondazione Prometeo chiede di portare 8 ragazzi del programma "Codice Aperto" in platea e di dare spazio sul palco al Presidente (on. Roberto Gabrielli) per consegna simbolica assegno. Discussione su tempistica, sicurezza minori, tono della presenza istituzionale.

### Messaggi chiave

**[2 nov, 10:19] Silvia Tartaglia (esterna) → Elena**
> Cara Elena, volevamo proporti:
> - 8 ragazzi (14-17 anni) del programma Codice Aperto, con 2 tutor, in platea riservata
> - breve intervento del Presidente Gabrielli (massimo 3 min) a metà evento
> - consegna simbolica assegno al fischio finale
>
> Ci aiuterebbe tantissimo per fundraising post-evento. Fammi sapere entro venerdì se fattibile.

**[2 nov, 14:56] Elena Moretti → Tommaso, Federica**
> Ragazzi, questa è gold narrativamente. MA:
> - bambini in platea → protocollo sicurezza diverso (minori, consenso genitori, privacy video)
> - intervento Presidente → cambia scaletta, serve logistica VIP
> - consegna assegno in chiusura → perfetto, zero attrito
>
> Vi chiederei di chiudere internamente entro mercoledì 4.

**[3 nov, 09:12] Barbara Russo (aggiunta in cc) → thread**
> Minorenni in platea: serve liberatoria firmata dai genitori (template standard, glielo mando io a Silvia), posti in zona sicura distanti almeno 2.5m dal campo. Fattibile.
> Privacy immagini: se vengono ripresi in broadcast, consenso esplicito per ciascuno. Cesta "no-face" se qualcuno non lo vuole.

**[4 nov, 17:41] Marco Bellini → thread**
> On. Gabrielli: va bene ma attenzione. Non deve sembrare una passerella politica. Scritto breve, scritto da noi, 2 min max letti. Tommaso, prepari tu il testo d'accordo con loro?
> Per l'assegno: CEO lo consegna insieme al Presidente. Simmetria voluta.

**[7 nov, 18:05] Tommaso Marchi → thread (chiusura)**
> Chiudo:
> - bambini confermati, 8 + 2 tutor, liberatorie in ricezione
> - Intervento Gabrielli: 2'30", bozza inviata a suo portavoce stamattina
> - Consegna: Gabrielli + Bellini insieme, duplicato assegno gigante per foto, assegno reale in busta
> - Media angle: STEM-for-all, non charity generica. Angolo coerente con DESaiN e copertura tech.

---

## Thread #32 — "DR2 issue tracker — 47 issue, prioritizzazione per ownership"
**Aperto**: 31 ott 2026, 07:14 · **Messaggi**: 31 · **Chiusura**: 15 nov 16:22
**Partecipanti**: Stefano Bianchi, Alessandro Conti, Luca Ferraresi, Federica Mazzarese, Barbara Russo, Andrea Moro + altri

**Sintesi**: post-DR2 si genera uno sheet condiviso (Google Sheets linkato) con 47 issue. Il thread serve per escalation e sblocchi. Le 6 issue bloccanti vengono tutte chiuse entro il 13/11.

### Estratto issue critiche (da allegato `dr2-issues-v3.xlsx`)

| # | Priorità | Descrizione | Owner | Status 15/11 |
|---|---|---|---|---|
| 01 | 🔴 Blocking | Ombre longitudinali zona B3-C3 | Stefano | ✅ Closed (Thread #30) |
| 02 | 🔴 Blocking | Latenza rete robot-referee box 180ms → target <80ms | Stefano | ✅ Closed (WiFi 6E + switch dedicato) |
| 03 | 🔴 Blocking | Ball tracking fallisce con telecamera broadcast a 50fps | Luca | ✅ Closed (filtro fps sync) |
| 04 | 🔴 Blocking | E-stop centrale non raggiunge K1-07 in 3 test su 10 | Stefano + Luca | ✅ Closed (ridondanza radio 433MHz) |
| 05 | 🔴 Blocking | Camera broadcast 4 angolo morto porta sud | Andrea | ✅ Closed (aggiunta cam 7) |
| 06 | 🔴 Blocking | Battery swap > 25 sec, target <15 sec | Luca | ✅ Closed (nuova procedura pit) |
| 07 | 🟠 High | Commentatore tecnico non ha ancora visto robot dal vivo | Tommaso | ✅ Closed (visita 14/11) |
| 08 | 🟠 High | Defibrillatore a bordocampo mancante | Barbara | ✅ Closed (acquisto + formazione) |
| 09 | 🟠 High | Scaletta apertura troppo lunga, 18 min | Alessandro | ✅ Closed (tagliata a 11 min) |
| 10-14 | 🟠 High | [altre 5 issue produttive] | vari | ✅ Tutti closed |
| 15-47 | 🟡 Medium / 🟢 Low | [33 issue di rifinitura] | vari | 28 closed, 5 accettate come non bloccanti |

### Messaggio chiave

**[15 nov, 16:22] Federica Mazzarese → thread (chiusura finale)**
> 42 su 47 chiuse. 5 accettate come "known minor" documentate nel log evento. Issue tracker congelato. Nuove issue da qui in avanti → canale `#warroom` esclusivamente.

---

## Thread #33 — "Embargo stampa — lista finale giornalisti, dichiarazioni pre-approvate, crisis statement"
**Aperto**: 5 nov 2026, 11:08 · **Messaggi**: 28 · **Chiusura**: 11 nov 09:58
**Partecipanti**: Tommaso Marchi, agenzia PR (Ketchum Italia — Federico Passarelli), Valeria De Santis, Federica Mazzarese, Marco Bellini

**Sintesi**: si definiscono 11 testate sotto embargo fino a mercoledì 11 novembre ore 10:00. Tre scenari di crisis comms pre-approvati.

### Messaggi chiave

**[5 nov, 11:08] Tommaso Marchi → thread**
> Proposta lista embargo:
>
> **Tier 1 (interviste 1:1 con Bellini + Suriani pre-evento)**
> - Corriere della Sera — Milena Gabanelli / sezione Innovazione
> - La Repubblica — Riccardo Luna
> - Sole 24 Ore — Luca De Biase
> - Wired Italia — Federico Ferrazza
>
> **Tier 2 (briefing collettivo embargato)**
> - ANSA Tecnologia, AGI Innovazione, RaiNews24, La7, Sky TG24, DDAY.it, Tom's Hardware
>
> Chiedo OK entro domani sera.

**[6 nov, 17:44] Federico Passarelli (Ketchum) → Tommaso**
> Lista ok. Ti allego:
> - talking points Bellini (2 pag)
> - talking points Suriani (scientific-pack, 3 pag)
> - Q&A antipatiche (15 domande preparate, incluso "perché spendere tanto se si poteva donare direttamente?")
>
> E soprattutto: allegato `crisis-statements-v2.docx` con 3 scenari pre-approvati.

**[7 nov, 15:12] Valeria De Santis → Tommaso (riservata)**
> Legale sul `crisis-statements-v2`: ho piccole revisioni sullo scenario 2 (infortunio dipendente). Parole come "responsabilità" vanno tolte, sostituite con "assistenza". Ti rimando tracciato.

**[11 nov, 09:58] Tommaso Marchi → thread (go-live)**
> Comunicato ufficiale va live alle 10:00. Embargo liftato. Social pack partito ai canali. GO GO GO 🚀

---

## Thread #34 — "Infortunio Silvia Ranzi in allenamento — sostituzione roster Human Squad"
**Aperto**: 8 nov 2026, 14:33 · **Messaggi**: 17 · **Chiusura**: 10 nov 21:15
**Partecipanti**: Giulia Peretti, Paolo "Pacio" Lopez (coach), Barbara Russo, medico sportivo (dr. Cavalli), HR Business Partner, Federica Mazzarese

**Sintesi**: Silvia Ranzi (product manager, terzino destro del roster titolare) si stira il polpaccio durante l'ultimo allenamento. 10 giorni di stop. Attivata prima riserva: Daniele Orsi (back-end eng). Coordinata la comunicazione interna per evitare drammi.

### Messaggi chiave

**[8 nov, 14:33] Pacio Lopez → Giulia, Barbara**
> Silvia out. Stiramento polpaccio dx al 32° di allenamento, prima che partisse la verticalizzazione. Niente di serio, 10 giorni, ma per il 21 è out sicuro. Entra Daniele dalla panchina.

**[8 nov, 16:02] dr. Cavalli → Barbara, Silvia in cc**
> Confermata diagnosi: stiramento I grado, 8-12 giorni. Tecar consigliata. Nessun referto di responsabilità, allenamento regolare, attrezzatura OK.

**[9 nov, 09:47] Giulia Peretti → HRBP, Federica**
> Gestisco io la comunicazione con Silvia. Le ho già scritto ieri sera. È delusa ma è testa forte. Le abbiamo proposto ruolo in regia + passaggio di testimonio a Daniele sul palco durante l'apertura. Ha accettato.

**[10 nov, 21:15] Federica → Giulia (chiusura informale)**
> Bravissima come hai gestito. Daniele già dentro, Silvia diventa ambassadress. È una win narrativa.

---

## Thread #35 — "Commentatore tecnico — shortlist finale e scelta"
**Aperto**: 9 nov 2026, 08:40 · **Messaggi**: 23 · **Chiusura**: 13 nov 17:28
**Partecipanti**: Tommaso Marchi, Chiara Volpe, Andrea Moro, agenzia PR, Federica Mazzarese

**Sintesi**: shortlist a 3 nomi, audition via Zoom su spezzone DR2, scelta su Giulia Bertagnolli (divulgatrice scientifica, ex Radio DeeJay Science, presenza tech conference).

### Messaggi chiave

**[9 nov, 08:40] Tommaso Marchi → thread**
> Shortlist finale:
>
> 1. **Giulia Bertagnolli** — divulgatrice scientifica, ex Radio DeeJay, 180k IG, inserzioni a WMF e ITW. Pro: voce, tono, zero paura del tecnicismo. Contro: cachet alto (€9k/day).
> 2. **Prof. Andrea Bonarini** — Politecnico Milano, storico RoboCup Italia. Pro: autorità. Contro: cadenza accademica, rischio pubblico si perda.
> 3. **Matteo Flora** — divulgatore cybersec noto. Pro: performativo. Contro: non specificamente robotica.
>
> Audition Zoom giovedì sera su spezzone DR2 (2 min commento a cieco). Voto aperto?

**[12 nov, 22:30] Andrea Moro → thread (post-audition)**
> Bertagnolli è oro. Ha capito il ritmo, sa quando tacere (fondamentale), ha improvvisato una metafora su "rete neurale come centrocampo" che funziona. Bonarini ha fatto una lezione bellissima ma di 4 minuti. Flora ha performato ma ha chiamato i robot "umanoidi" per 2 volte — cosa che infastidirebbe la comunità tecnica.
>
> Mia scelta: Bertagnolli.

**[13 nov, 17:28] Federica Mazzarese → thread**
> Confermo Bertagnolli. Tommaso chiudi contratto. Brief tecnico con Luca + Vincenzo il 17/11 sera.

---

## Thread #36 — "Polizza assicurativa — firma finale + rider eccezioni"
**Aperto**: 10 nov 2026, 10:15 · **Messaggi**: 13 · **Chiusura**: 12 nov 16:44
**Partecipanti**: Valeria De Santis, Barbara Russo, broker (Marsh Italia — Paolo Tresoldi), Federica Mazzarese

**Sintesi**: firma finale polizza RC eventi + infortuni partecipanti + danni hardware. Rider aggiunto last-minute per bambini in platea (Fondazione Prometeo).

### Messaggi chiave

**[10 nov, 10:15] Valeria De Santis → broker**
> Paolo, due update:
> 1. confermata presenza 8 minori (14-17) in platea dedicata → serve estensione di RC
> 2. rider danni hardware robot lo confermiamo a €250k cap come discusso
>
> Ci serve polizza firmata entro mercoledì per rilascio finale venue.

**[11 nov, 18:20] Paolo Tresoldi → Valeria**
> Rider minori aggiunto, massimale €2M unitario. Costo +€780. Rider hardware confermato €250k. Polizza completa: €14.320 + IVA. Documento in firma digitale.

**[12 nov, 16:44] Valeria De Santis → thread (chiusura)**
> Firmata. Consegnata a venue manager. Chiudo thread.

---

## Thread #37 — "Run of Show v47 FINAL — distribuzione a tutti i Lead"
**Aperto**: 14 nov 2026, 21:03 · **Messaggi**: 9 · **Chiusura**: 16 nov 11:12
**Partecipanti**: Alessandro Conti → a tutti (broadcast a 38 persone)

**Sintesi**: distribuzione del Run of Show definitivo (12 pagine, minutaggio secondo per secondo per broadcast). Feedback minimo, 3 ritocchi accettati.

### Messaggi chiave

**[14 nov, 21:03] Alessandro Conti → all-leads@**
> Allegato: `ros-v47-FINAL.pdf`.
>
> Cambi rispetto a v46:
> - apertura ridotta da 11' a 9'30" (taglio video secondario)
> - sigla ingresso team robot spostata a +0'45"
> - stacco pubblicità charity aggiunto a 24° min
> - cerimonia di chiusura: duplice consegna assegno Bellini + Gabrielli
>
> Qualunque modifica va richiesta entro sabato 15 ore 20:00. Dopo: FREEZE.

**[15 nov, 14:22] Tommaso Marchi → Alessandro**
> Una sola. Possiamo anticipare di 2 minuti il plug Fondazione all'apertura? Serve per taglio social del giorno.

**[15 nov, 18:49] Alessandro Conti → Tommaso**
> Ok ma no ulteriori modifiche. Spedisco v47.1 stanotte.

**[16 nov, 11:12] Alessandro → all-leads (chiusura)**
> v47.1 distribuita. **FROZEN.**

---

## Thread #38 — "Allineamento finale con CEO — briefing 18/11"
**Aperto**: 15 nov 2026, 10:44 · **Messaggi**: 6 · **Chiusura**: 17 nov 19:00
**Partecipanti**: Marco Bellini, Federica Mazzarese, exec assistant CEO

**Sintesi**: organizzazione briefing 45 min con CEO per allineamento finale. Preparato pack sintetico.

### Messaggio chiave

**[17 nov, 19:00] Federica Mazzarese → Marco Bellini (privato)**
> Pacchetto per CEO domani:
> - 1 pagina status (verde/giallo/rosso per area)
> - 1 pagina talking points press
> - 1 pagina "cosa può andare male e cosa facciamo"
> - 1 pagina fondazione + simbolica
>
> 45 min esatti. Domande principali attese: costo totale, ROI reputazionale, rischio legale. Ho le risposte. Sereno.

---

## Thread #39 — "Accrediti finali — giornalisti, VIP, partner"
**Aperto**: 16 nov 2026, 09:00 · **Messaggi**: 18 · **Chiusura**: 19 nov 23:48
**Partecipanti**: Venue Manager, Tommaso Marchi, Chiara Volpe, security partner, Elena Moretti

**Sintesi**: finalizzazione accrediti, badge, zone, pass parking. Crisi minore: 6 richieste last-minute di cui 3 accolte.

### Messaggio chiave

**[19 nov, 23:48] Chiara Volpe → thread (chiusura)**
> Accrediti finali:
> - 34 stampa (tier 1+2)
> - 82 dipendenti squadra + staff
> - 48 VIP/partner
> - 12 Fondazione (inclusi ragazzi + tutor + famiglie autorizzate)
> - 6 institutional (incluso Presidente Gabrielli)
> - 420 dipendenti pubblico
> - 180 ospiti esterni (lottery interna)
> **Totale**: 782 accrediti. Capienza max 1.100 → siamo a 71%.

---

## Thread #40 — "Walkthrough finale 20/11 — ordine del giorno e convocazione"
**Aperto**: 19 nov 2026, 18:30 · **Messaggi**: 7 · **Chiusura**: 20 nov 07:45
**Partecipanti**: tutti i Lead + TD + coach Human Squad + SPQR

**Sintesi**: walkthrough finale in venue venerdì 20 novembre, 14:00-22:00. Tutti in sede. Format: walkthrough scaletta + smoke test + cena di squadra.

### Messaggio chiave

**[19 nov, 18:30] Federica Mazzarese → all-leads**
> Domani 20/11:
>
> **14:00** ritrovo Fiera di Roma Padiglione 6, ingresso artisti
> **14:30–17:30** walkthrough scaletta minuto per minuto con tutti i presenti in scena
> **17:30–19:00** smoke test tecnico (no game, solo boot + sync + comms)
> **19:00–20:30** briefing sicurezza con Barbara (obbligatorio)
> **20:30** cena al ristorante "Le Margheritine" (convocazione 28 persone, copertura aziendale)
> **22:00** rientro e silenzio stampa interno fino a sabato 10:00
>
> Nessuna assenza tollerata se non per forza maggiore. A domani.
>
> — Fede

---

## Note di metaprocesso

- **Volume**: 23 thread nuovi in 30 giorni (+ 47 thread vecchi riattivati). Media: ~4 thread/giorno di media da rispondere.
- **Tempo di risposta medio dei Lead**: 3h11' (misurato su campione 80 messaggi). Dentro SLA interno informale di 4h diurne.
- **Thread più lungo in messaggi**: #32 issue tracker (31 messaggi su 15 giorni).
- **Thread più breve risolutivo**: #38 CEO briefing (6 messaggi, 48h).
- **Email con più destinatari**: #40 walkthrough finale (38 destinatari).
- **Nessuna email inviata dopo le 23:00** per policy informale del PD (escalation via Slack, vedi `colleague-chats.md`).
