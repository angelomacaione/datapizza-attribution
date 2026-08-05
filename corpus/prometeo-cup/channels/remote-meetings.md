# remote-meetings.md
**Periodo**: T-1 mese → T-1 giorno (21 ottobre → 20 novembre 2026)
**Piattaforme**: Microsoft Teams (default aziendale) · Zoom (con esterni) · Google Meet (con Sapienza)
**Totale meeting in periodo**: 68 · Qui documentati i 9 principali + 1 recurring

---

## Setup ricorrente

**Lunedì 09:00–09:30** — *Leadership stand-up* (tutti i Lead + PD + Sponsor via DM notes)
**Mercoledì 10:00–10:45** — *Robot Squad sync* (Luca, Vincenzo + SPQR PhD)
**Venerdì 16:00–16:30** — *Risk review* (Barbara, Valeria, Federica)
**Ultimo giovedì mese 17:00–18:30** — *Steering committee* (Sponsor + Lead + CFO)

Registrazioni: attivate solo su richiesta, conservate 90 gg in SharePoint. Note obbligatorie in Confluence pagina meeting.

---

## 1. Leadership stand-up — lunedì 27 ottobre 2026, 09:00 (esempio ricorrente)
**Piattaforma**: Teams
**Durata**: 31 min (over di 1')
**Partecipanti**: Federica, Luca, Giulia, Alessandro, Barbara, Elena, Tommaso, Valeria + Stefano (ospite)
**Formato**: round robin 2' a testa + blockers + decisioni

### Note
- **Federica**: settimana pre-DR2, priorità 1 sul freeze codice SPQR. Priorità 2 gestione stampa in embargo. Sponsor rassicurato, nessuna escalation C-level questa settimana.
- **Luca**: codice SPQR in freeze martedì 18:00. Due K1 rientrati sabato, terzo in DHL. Rental K1 da GR confermato.
- **Giulia**: roster allenamenti al completo, Silvia in rientro dopo tacar sessione pregressa (precauzionale). Coach Pacio segnala bisogno di 1 sessione in più in venue se disponibile → chiedere a Alessandro.
- **Alessandro**: walk-through DR2 in pulito martedì 28. Scaletta v44 distribuita. Serve decisione su cerimonia apertura (opening video 3' o 5').
- **Barbara**: RSPP ha chiuso DVR evento venerdì. Defibrillatore arriva lunedì. Medico confermato. Un punto aperto: chi è il "Safety Officer in campo" — deve essere persona dedicata il giorno, non cumulo ruoli. Candidata: Francesca Trombetta, RSPP senior da contratto.
- **Elena**: Silvia Tartaglia (Fondazione) propone portare 8 ragazzi e Presidente Gabrielli in evento. Complesso ma potentissimo narrativamente. Passa in thread dedicato #31.
- **Tommaso**: lista giornalisti Tier 1+2 in chiusura questa settimana. Embargo al 11/11.
- **Valeria**: contingency al 72%, delta previsto su illuminazione (vedi thread #30 se esce). Polizza in firma settimana prossima.
- **Stefano** (ospite): DR2 tecnico: serve accesso padiglione dalla domenica 27 ottobre ore 6:00. Conferma con Venue Manager.

### Decisioni
1. **Opening video**: si decide 4'30" intermedio (Alessandro delega a Chiara).
2. **Sessione allenamento in venue**: concessa, giovedì 5 novembre ore 20:00, campo pulito post-installazione luci.
3. **Safety Officer in campo**: ok a Trombetta, contratto in bozza entro giovedì.
4. **Ragazzi Fondazione**: procedere, Elena + Barbara co-owner.

### Blockers da portare in Steering
- Nessuno questa settimana. Eventualmente il delta budget luci dopo DR2.

---

## 2. DR2 — Briefing tecnico pre-dry run — mercoledì 28 ottobre 2026, 14:00
**Piattaforma**: Google Meet (per includere SPQR)
**Durata**: 1h 47min
**Partecipanti**: Luca, Vincenzo, 3 PhD SPQR (Giacomo, Elisa, Matteo), Stefano, Andrea Moro, Barbara, Federica (osservatrice)

### Agenda
1. Stato codice freezato (15')
2. Walkthrough scenari DR2 (40')
3. Gestione fallimenti previsti (30')
4. Protocollo e-stop e comunicazioni (20')

### Note chiave

**Stato codice (Vincenzo)**
> "Tag `hsl-2026-dr2-v1` è in freeze. Unica cosa instabile è la policy di goal approach del portiere: in simulazione gira al 94%, ma in laboratorio ha dato un falso positivo. Lo dichiaro come rischio accettato. Se succede in campo, il portiere si butta sul nulla e noi ridiamo. Charm rispetto a catastrofe."

**Scenari di fallimento (Luca + Vincenzo)**
- *Robot a terra che non si rialza* → protocollo recovery autonoma tentata 2 volte, poi pit crew entra a campo fermo (50/50 di occorrenza nel match)
- *Kernel panic Jetson* → hot-swap su Jetson spare (15-20" fermo)
- *Perdita rete globale* → e-stop automatico, tutti i robot standby, riprendere game dopo max 60"
- *Palla fuori campo* → ball boy umano (ruolo già assegnato, 2 persone)

**E-stop (Stefano + Barbara)**
- Sistema a 3 livelli: (1) soft via SDK, (2) hard via referee box, (3) radio dedicata 433 MHz (nuovo post-DR1)
- Barbara come Safety Officer: ha il trigger del livello 3 accanto a sé. Nessun altro.

**Domanda di Andrea Moro (broadcast)**
> "Se chiamiamo e-stop, il broadcast cosa fa?"

Decisione: cartello grafico "⚙️ Tecnical pause — il gioco riprende a breve" + voce Bertagnolli che riempie. Pre-registrata una clip di Vincenzo che spiega il comportamento dei robot (fallback contenuto).

### Action items
- [Luca] smoke test rete con SSID separati entro venerdì 30
- [Stefano] e-stop drill con tutti presenti in DR2
- [Andrea] cartello grafico e pre-roll Vincenzo entro lunedì 3/11
- [Vincenzo] post-DR2 debrief short entro venerdì 30 sera

---

## 3. DR2 debrief — sabato 31 ottobre 2026, 10:00
**Piattaforma**: Teams (ibrido, 8 in sala + 4 remote)
**Durata**: 2h 18min (over di 48 min)
**Partecipanti**: tutti i Lead + Vincenzo + 2 PhD SPQR + Andrea Moro + Massimiliano (Luce Eventi, aggiunto alle 11:30)

### Stato
- 2 cicli di match su 3 completati in DR2 (67% success rate)
- 47 issue aperte nel tracker (vedi thread #32)
- 6 bloccanti, 14 alte, 27 medie/basse

### Note

**Federica (apertura)**
> "Non abbiamo perso niente di fatale. Abbiamo imparato 47 cose in un pomeriggio. È esattamente per questo che facciamo il DR2. L'obiettivo del prossimo walkthrough è avere zero bloccanti aperte. Non parliamo di prestazione, parliamo di rischio."

**Principale scoperta inattesa**: le ombre longitudinali (già citato thread #30). Nessuno l'aveva visto perché in sopralluoghi precedenti le luci erano diverse.

**Punto controverso**: Vincenzo propone di **disinstallare la policy portiere** e usare un "dummy keeper" fisso in porta. Riduce rischio ma toglie uno dei momenti più spettacolari possibili.

Dibattito 22 minuti. Decisione: teniamo la policy ma la declassiamo (soglia di attivazione più bassa, il portiere rimane più spesso fermo, esce solo su palla chiara). Compromesso tecnico.

**Massimiliano arriva alle 11:30** per consulenza lampo su illuminazione. Dato mandato: proposta entro lunedì.

### Decisioni
1. DR3 non si fa. (Era nel piano ma il tempo non c'è: walkthrough del 20/11 come unica prova finale.)
2. Policy portiere modificata: soglia attivazione 0.6 → 0.3.
3. Illuminazione: decisione entro lunedì 2/11 con opzioni Massimiliano.
4. Tutte le 6 issue bloccanti devono essere chiuse entro venerdì 13/11.

### Clima
A fine meeting Federica propone venerdì dopo lavoro spritz ai Lead (offerta aziendale). Accettano tutti tranne Luca che ha figlio malato. Piccola cosa, conta.

---

## 4. Steering Committee (ultimo prima evento) — giovedì 5 novembre 2026, 17:00
**Piattaforma**: Teams
**Durata**: 1h 33min
**Partecipanti**: Marco Bellini (CHRO), Federica, CFO (Alberto Marini), CIO, CEO (solo in coda 12 min), tutti Lead

### Agenda
1. Dashboard semafori (15')
2. Status budget (20')
3. Issue aperte e rischi residui (30')
4. Ingresso CEO + Q&A (25')

### Highlight dashboard

| Area | Status | Note |
|---|---|---|
| Hardware | 🟡 | 1 K1 ancora in transito, backup coperto |
| Software | 🟢 | Codice freezato, DR2 passato |
| Venue & Produzione | 🟡 | Illuminazione in fix, delta budget 28k |
| Safety & Medical | 🟢 | Tutto in place, DVR chiuso |
| Charity | 🟢 | Fondazione + Presidente allineati |
| Comms & PR | 🟢 | Embargo in corso, go-live 11/11 |
| Legal & Finance | 🟡 | Polizza in firma, contingency 54% (era 72%) |
| Human Squad | 🟡 | Infortunio Silvia, Daniele entra |

### Domanda CFO (punto tecnico sentito)
> "Contingency al 54% con 16 giorni dall'evento. Storicamente si brucia ancora 10-15% negli ultimi giorni. Siamo davvero tranquilli?"

**Risposta Federica**: "No, non siamo tranquilli, siamo consapevoli. Abbiamo identificato i 3 punti di rischio ulteriore: (a) ulteriori guasti hardware improvvisi, (b) sostituzione last-minute broadcast, (c) costi meteo non previsti. Totale esposizione residua stimata €60-90k. Coperti dalla contingency rimanente."

### CEO (intervento finale)
> "Mi avete convinto tre mesi fa e mi state convincendo ora. L'unica cosa che vi chiedo è: se succede qualcosa il giorno, la persona che va davanti alle telecamere è Marco. Non io. Noi abbiamo fiducia in voi, la catena di comando dev'essere una. Chiaro?"
>
> Federica: "Chiaro."

### Decisioni Steering
1. Go evento confermato.
2. Sponsor Bellini è PRIMA VOCE aziendale in caso crisi. CEO silenzio media day-of.
3. Budget delta luci approvato.
4. Prossimo Steering: post-mortem, giovedì 10 dicembre.

---

## 5. Briefing stampa embargato — martedì 10 novembre 2026, 15:00
**Piattaforma**: Zoom (stampa esterna)
**Durata**: 55 min (pianificati 45')
**Partecipanti**: Marco Bellini, Vincenzo Suriani, Elena Moretti, Federica, Tommaso, Federico (Ketchum), 11 giornalisti

### Struttura
- Intro Tommaso (3')
- Bellini: perché l'azienda (8')
- Vincenzo: la parte scientifica (10')
- Elena: la charity (6')
- Q&A (28')

### Domande interessanti (estratto)

**Milena Gabanelli (Corriere)**:
> "Perché non avete semplicemente donato i 600 mila euro?"

Risposta Bellini (allineata):
> "Tre ragioni. Prima: visibilità moltiplicata del messaggio STEM. Stima PR che ci dà 3-5x l'impatto mediatico di una donazione tradizionale. Seconda: il coinvolgimento dei nostri dipendenti crea cultura interna che dura oltre l'evento. Terza — e questa è la meno raccontabile ma è vera: portare robot autonomi in uno spettacolo aperto al pubblico abbassa il muro tra ricerca e società. Questo era scritto nella missione di Prometeo prima ancora che partissimo. Fanno loro il lavoro educativo durante tutto l'anno. Noi lo amplifichiamo una sera."

**Riccardo Luna (Repubblica)**:
> "Quanti gol pensate di prendere?"

Risposta Vincenzo (rilassata):
> "Dai 10 ai 20. I robot autonomi del 2026 non sono ancora pronti per competere con umani, tutti nell'ambiente lo sappiamo. La partita non è tecnica, è culturale. E poi nel 2050 vi ricontatteremo per l'intervista di follow-up."

### Valutazione Tommaso post-call
> "Andata bene. Zero domande gotcha. Gabanelli era quella che temevo e ha fatto il suo mestiere seriamente. Embargo tiene, ne sono ragionevolmente sicuro."

---

## 6. Risk Review straordinaria — giovedì 12 novembre 2026, 18:30
**Piattaforma**: Teams
**Durata**: 44 min
**Partecipanti**: Barbara, Valeria, Federica, Luca, Stefano (ospite)

### Motivo
Durante scouting finale dell'hall adiacente (padiglione 7, sta ospitando fiera dell'ottica in contemporanea), emerge che il loro WiFi è ad alta densità e potrebbe interferire con la nostra rete dedicata. Serve decisione in 48h.

### Note
**Stefano**:
> "Ho fatto RF survey oggi pomeriggio con analyzer. Sul canale 6 e 11 abbiamo congestione al 67% che arriva dal padiglione 7. Noi usiamo canale 149 (5 GHz) quindi tecnicamente siamo OK, ma se saltiamo in 2.4 per emergenza, saremmo in overlap con loro."

**Decisioni**
1. Lockdown completo della nostra rete sul 5GHz canale 149, disabilitazione 2.4 per tutti i dispositivi robot.
2. Coordinamento con venue manager padiglione 7: loro silent period sul 5GHz durante match (10:30-17:30 del 21/11). Negoziazione via Venue Manager.
3. Piano C: se tutto salta, passiamo a rete cablata diretta dal referee box ai robot (Cat6A già predisposto come backup, mai usato).

### Nota emotiva
Barbara a fine call:
> "Stefano, grazie. Questa è la quarta volta che ti accorgi di un problema che nessuno ci aveva chiesto. Fai la differenza."

---

## 7. Robot Squad — ultima sync prima del walkthrough — mercoledì 18 novembre 2026, 10:00
**Piattaforma**: Google Meet
**Durata**: 1h 12min
**Partecipanti**: Luca, Vincenzo, 4 PhD SPQR, Stefano (prime 30')

### Stato finale

| Robot | Status | Note |
|---|---|---|
| K1-01 | 🟢 Pronto | Calibrato in laboratorio |
| K1-02 | 🟢 Pronto | |
| K1-03 | 🟢 Pronto | Rientrato da repair 27/10 |
| K1-04 | 🟢 Pronto | |
| K1-05 | 🟢 Pronto | |
| K1-06 | 🟢 Pronto | |
| K1-07 | 🟡 Osservazione | Giunto ginocchio dx con gioco 0.3mm, sotto tolleranza ma da monitorare |
| K1-08 | 🟢 Pronto | Rientrato 30/10 |
| K1-09 | 🟢 Pronto | Rental Génération Robots, consegnato 5/11 |
| K1-10 | 🟢 Pronto | |
| K1-spare | 🟢 Pronto | Coperto da uno dei 10 in rotazione |
| NAO-01 a 03 | 🟢 Pronto | Backup, non schedulati in scaletta |

### Code freeze
Conferma: nessuna modifica al codice da giovedì 13 ore 18:00. Tag `hsl-2026-final-v2.1`.

### Rituale pre-match (proposto da Vincenzo)
> "Ho un'idea un po' stupida. Facciamo una foto squadra venerdì mattina. Dieci robot schierati, il team umano SPQR e di sistemi dietro. Manderemo a Booster e a RoboCup Federation come omaggio. Mi piace perché ci ricorda perché lo facciamo."

Accettata. Chiara Volpe ci farà uscire un contenuto social dopo l'evento.

### Ultimo commento Luca
> "Vincenzo, nei nostri 7 mesi non ti ho mai detto grazie in modo esplicito. Lo faccio ora. Questa cosa senza SPQR non esisteva. Grazie."

---

## 8. All-Hands finale — venerdì 20 novembre 2026, 14:30 (ibrido)
**Piattaforma**: ibrido, 28 in sala venue + 14 remoti
**Durata**: 1h 45min
**Partecipanti**: tutto lo staff core + day-of Lead

### Struttura
- Walkthrough scaletta minuto per minuto (1h)
- Briefing sicurezza (Barbara) (30')
- Discorso di Federica (10')
- Cerimonia (5')

### Discorso Federica (trascrizione approssimata)
> "Allora. Domani alle 16:00 si fischia.
>
> Abbiamo preparato questo per 7 mesi. Ognuno di voi, nel proprio angolo, ha costruito un pezzo che da solo è complesso e che insieme diventa... questa cosa qui, che credo sia senza precedenti in Italia.
>
> Domani qualcosa andrà storto. Lo sappiamo. Abbiamo piani per quasi tutto e piani anche per l'imprevisto. Il nostro lavoro, adesso, non è far sì che tutto vada perfetto. Il nostro lavoro è farci trovare pronti quando qualcosa non va, restare lucidi, e comunicare subito sulla war room.
>
> Due cose che vi chiedo esplicitamente.
>
> **La prima**: se avete un dubbio, anche stupido, anche piccolo, lo dite. Non c'è domanda stupida domani. C'è solo la domanda non fatta che diventa incidente.
>
> **La seconda**: guardatevi negli occhi. Avete visto tutti quante persone ci sono qui. Siamo in 75 nel core, più altri 200 sul campo domani, più 2000 persone in platea, più centinaia di migliaia che ci guarderanno dopo. Ma il centro di tutto questo sono 8 ragazzi che stanno facendo il corso di coding della Fondazione Prometeo. Lo scopo di tutto questo è loro. Se domani alle 18:00 la Fondazione ha i soldi per tre anni di programma, abbiamo vinto, qualunque sia il risultato della partita.
>
> Grazie per questi 7 mesi. Ci vediamo domani mattina alle 7:00 in venue, caffè pagato da Elena. A dopo."

### Cerimonia
Consegna di una pin simbolica (design di Chiara) a ogni membro del core team. 28 pin. Silvia Ranzi riceve la sua a distanza, videocall.

### Fine meeting
- 19:00 smoke test tecnico
- 20:30 cena di squadra al ristorante "Le Margheritine"
- 22:00 rientro

---

## 9. Briefing ultimo — venerdì 20 novembre 2026, 22:30
**Piattaforma**: Teams, 15 minuti
**Partecipanti**: Federica, Marco Bellini, Tommaso, Barbara, Alessandro

### Nota
Non era programmato. Federica lo convoca dopo cena, su 5 persone strette.

### Motivo
Una segnalazione sulla chat WhatsApp #robot-squad-leaders: un operatore del venue ha notato un piccolo incendio in un cestino nel pad 6 alle 21:00, spento in 30 secondi da vigili del fuoco presenti. Nessun danno. Nessun coinvolgimento con setup evento. Ma: serve sapere se è il caso di cambiare qualcosa all'apertura di domattina.

### Decisione
- Barbara fa sopralluogo personale alle 07:00 di sabato con Responsabile Venue.
- Nessuna modifica allo scouting. Nessun comunicato. Si tratta di operatività venue standard.
- Federica: "Da adesso silenzio mentale. Ci vediamo domani. Buonanotte davvero. Dormite."

---

## Totale meeting in periodo

| Tipo | N. |
|---|---|
| Stand-up settimanale | 4 |
| Robot Squad sync ricorrente | 4 |
| Risk Review ricorrente | 4 |
| Steering Committee | 1 (+ 1 straordinario Oct) |
| DR2 + debrief | 2 |
| Press briefings (stampa) | 3 (Tier1 1:1 + collettivo) |
| Bilaterali Federica-Lead | 19 |
| Emergenza / crisi | 6 |
| Onboarding commentatore, fornitori | 4 |
| Partnership SPQR bilaterali | 6 |
| Cerimonie formali (all-hands, farewell) | 2 |
| Walkthrough finale | 1 |
| Briefing last-minute | 2 |
| **Totale periodo** | **68** |

### Metrica osservata
Federica spende **~11 ore/giorno in meeting** nei primi 20 giorni del periodo (dato da Outlook Calendar Analytics). Negli ultimi 10 giorni scende a ~7h/giorno, compensate da 3h di deep-work quotidiane (blocchi dedicati nel calendario difesi esplicitamente).
