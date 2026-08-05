# Prometeo Cup — Obsidian Vault

Generato automaticamente da 6 file narrativi di canale comunicazione.

## Come usarlo

1. **Installa Obsidian** (https://obsidian.md)
2. Apri Obsidian → **Open folder as vault** → scegli questa cartella
3. Apri `00-Index.md` come punto d'ingresso
4. Premi **Cmd+G** (macOS) o **Ctrl+G** (Win/Linux) per il Graph View
5. Nel Graph View, nel pannello laterale:
   - Filtra per tag (`#person`, `#org`, `#milestone`, `#thread`)
   - Raggruppa per cartella (colore diverso per people/orgs/ecc.)
   - Alza la forza di repulsione per spacing più chiaro

## Struttura

```
00-Index.md                 ← parti da qui
channels/                   ← i 6 file originali narrativi
people/                     ← una nota per ciascuna persona
organizations/              ← partner, fornitori, fondazione
milestones/                 ← eventi-chiave del processo
tech/                       ← hardware e tecnologie citate
threads/                    ← thread email #28..#40
```

## Come si estende

Rilancia `build_vault.py` dopo aver:
- aggiunto nuovi file .md in `channels/`
- aggiornato i dizionari PEOPLE/ORGS/MILESTONES/TECH nello script

## Plugin Obsidian consigliati

- **Dataview** — query tipo DB sul vault
- **Graph Analysis** — centralità, community detection
- **Breadcrumbs** — relazioni tipate gerarchiche
- **Juggl** — graph interattivo avanzato con filtri

## Limitazioni di questa estrazione

- Co-occorrenze calcolate per file, non per sezione (approssimazione)
- Nessuna relazione tipata (Federica *decide* X, SPQR *fornisce* Y):
  per questo servirebbe estrazione semantica (Neo4j + LLM)
- Nessun linking cross-entity automatico nei file-canale
  (i canali rimangono testo pulito, non editato)
