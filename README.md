# Superficie di attribuzione

Prototipo di interfaccia: mostra su cosa poggia una risposta generata, quanto è solida, e cosa manca per firmarla.

**Live:** [datapizza.amaca.design](https://datapizza.amaca.design)

Un file HTML, nessun framework. L'unica risorsa esterna sono i webfont.

## Da dove vengono i dati

Dal test tecnico pubblico di Datapizza ([`datapizzaorg-ai-lab/test-tecnico-frontend-engineer`](https://github.com/datapizzaorg-ai-lab/test-tecnico-frontend-engineer)), eseguito davvero: `datapizza-ai` da PyPI, backend su uvicorn, login, upload dei tre PDF hash-validati, una run reale.

Quello che ne è uscito, e che l'artefatto serve come fixture senza riscriverlo:

- 432 chunk NDJSON dello stream
- 3 citazioni, 19 regioni con le loro `rects_in` in pollici
- il testo di tutte e 19 le regioni, **estratto dai PDF reali a quelle coordinate** con PyMuPDF — nel payload `text_quote` è un segnaposto, qui è il testo che sta davvero lì

**I contenuti sono mock.** La risposta parla di conformità, il corpus sono tre paper di informatica: lo squilibrio appartiene alla fixture di test, ed è dichiarato in apertura dell'artefatto.

## L'idea

Una risposta generata arriva con le citazioni allegate. Ma "ci sono le citazioni" e "l'affermazione regge" sono due domande diverse, e la seconda può essere falsa mentre la prima è vera. L'artefatto le tiene separate:

- **Integrità della citazione** — il testo è davvero a quelle coordinate, in quella pagina, in quel documento? Verificato rileggendo il PDF: 19 su 19.
- **Appoggio all'affermazione** — quel testo sostiene *questa* affermazione? Verificabile, sintesi inferita, o assente.

Una citazione perfettamente localizzabile può non reggere nulla. Fondere i due assi in un punteggio unico nasconde proprio il caso che interessa a chi deve firmare.

Ne segue una regola più stretta per le asserzioni di stato. Una riga come *Cifratura dati: OK* non asserisce un tema, asserisce un **verdetto**: che un documento parli di cifratura non dice che la cifratura sia a posto. Perché regga, l'evidenza deve pronunciare il verdetto, non toccare l'argomento.

Sui dati reali, calcolato e non messo in scena: le due affermazioni in prosa risultano sintesi inferita (0.90 e 0.80), e le **due righe della tabella — le uniche che si firmano — risultano senza appoggio**, pur avendo 19 citazioni verificabili allegate.

## Cosa è del loro contratto e cosa è proposto

Il payload di oggi porta `document_id`, `filename`, `page_number`, `text_quote`, `bounding_regions`: i campi che dicono **dove** guardare.

L'estensione proposta aggiunge `presence_verified`, `support_type`, `confidence`, `claim_id` — quest'ultimo perché oggi le citazioni sono attribuite alla risposta intera, non alla singola affermazione. L'artefatto distingue le due cose a schermo, e il pannello del metodo spiega come ogni valore è calcolato.

Il calcolo è deterministico e rieseguibile: nessuna chiamata a modello. Il ponte lessicale italiano-inglese, necessario perché la risposta è in italiano e il corpus in inglese, è dichiarato invece che implicito. Soglie e termini di verdetto sono dati, non codice: cambiano per normativa e per cliente, il componente resta uno.

## Note di realizzazione

I colori non sono stati scelti a mano. Il design system di Datapizza è stato compilato nel canonical del [compilatore Amaca](https://amaca.design) — 143 token, adapter DTCG — e questa interfaccia è una proiezione di quel canonical: ogni colore a schermo è un loro token chiamato per nome. I due assi stanno su famiglie diverse apposta: l'appoggio su `pastelgreen`, `yellow`, `red`; l'integrità su `azure`; la selezione su `blueribbon`.

**Tipografia e spaziatura non esistono nei loro token** — la copertura le dà aperte, e i loro custom properties infatti non ne contengono. Il carattere viene dai computed styles del sito (Inter, Space Mono) e la scala di spaziatura è mia. Nel foglio di stile sono marcate come tali, in un blocco separato, invece di essere presentate come loro.

Il colore non porta mai il significato da solo: ogni stato ha etichetta e icona. `prefers-reduced-motion` e `:focus-visible` sono gestiti, e tutte le coppie testo-sfondo passano AA. Verificato con jsdom, 75 controlli — inclusi i gate di provenienza che rifiutano un esadecimale che non esista nel canonical — più un passaggio su Chromium headless senza errori in console.

---

Costruito da [Angelo Macaione](https://angelomacaione.com). Design system open-source: [amaca.design](https://amaca.design).
