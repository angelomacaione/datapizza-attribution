#!/usr/bin/env python3
"""
Impagina la demo in un unico file HTML, con i dati veri dentro.

    python3 scripts/build_demo.py

Legge apps/web/demo-data.json e scrive apps/web/index.html: nessuna
dipendenza, nessun server, si apre con un doppio clic. Colori e caratteri
vengono dai token del design system di Datapizza (tokens.css).

La pagina e' una chat sull'archivio Prometeo Cup. Le risposte precalcolate
sono quattro; a una domanda diversa la chat risponde che non ce l'ha, invece
di inventare. E' una demo statica e lo dice.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATI = ROOT / "apps" / "web" / "demo-data.json"
USCITA = ROOT / "apps" / "web" / "index.html"

# Token presi da tokens.css del design system Datapizza.
# I quattro stati non esistono nel loro sistema: due li mappo sui loro token
# (destructive per il rosso, chart-2 per l'arancione), due li aggiungo qui e li
# segnalo come aggiunta locale invece di far finta che fossero gia' li'.
TOKENS = """
    /* --- da tokens.css di Datapizza -------------------------------- */
    --background:#fff; --foreground:#111827; --card:#fff; --border:#e5e7eb;
    --muted:#f3f4f6; --muted-foreground:#6b7280; --primary:#d87943;
    --primary-foreground:#fff; --secondary:#527575; --destructive:#ef4444;
    --radius:.75rem; --spacing:.25rem;
    --font-mono:"JetBrains Mono",ui-monospace,monospace;
    --font-sans:ui-monospace,monospace;
    /* font-serif esiste nel canonical ma vale "serif": una bare generic stack,
       che la loro stessa guida marca come finding. Le parti discorsive si
       distinguono con peso, dimensione, colore e tracking, non con una
       famiglia estranea al sistema. */
    --chart-1:#5f8787; --chart-2:#e78a53; --chart-3:#fbcb97;
    --shadow-sm:0px 1px 4px 0px #0000000d,0px 1px 2px -1px #0000000d;
    --shadow-md:0px 1px 4px 0px #0000000d,0px 2px 4px -1px #0000000d;
    --shadow-lg:0px 1px 4px 0px #0000000d,0px 4px 6px -1px #0000000d;

    /* --- i quattro stati ------------------------------------------- */
    /* rosso e arancione escono dai loro token; verde e blu non esistono
       nel sistema Datapizza e li aggiungo qui, accordati sul teal --chart-1 */
    --st-verde:#2f7d5d;      --st-verde-bg:#eaf5f0;
    --st-blu:#4a6fa5;        --st-blu-bg:#eef2f9;
    --st-rosso:var(--destructive);   --st-rosso-bg:#fdeeee;
    --st-arancione:var(--chart-2);   --st-arancione-bg:#fdf2e9;
"""

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
/* Le due famiglie hanno ruoli opposti: JetBrains Mono (l'unica davvero
   caricata) porta la voce del sistema — tesi, etichette, spiegazioni, note.
   Il monospace di sistema porta tutto cio' che viene dall'archivio o lo
   indirizza: la risposta sotto esame, le prove, i chip, gli offset. Cosi' si
   distingue a colpo d'occhio cio' che dice l'archivio da cio' che dico io. */
body{background:var(--muted);color:var(--foreground);font-family:var(--font-mono);
  font-size:15px;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1200px;margin:0 auto;padding:calc(var(--spacing)*7)}

/* --- istruzioni ---------------------------------------------------- */
.hero{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);
  padding:calc(var(--spacing)*6) calc(var(--spacing)*7);margin-bottom:calc(var(--spacing)*4);
  box-shadow:var(--shadow-sm)}
.eyebrow{font-size:11px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--primary);font-weight:600;margin-bottom:calc(var(--spacing)*2)}
.hero h1{font-size:21px;line-height:1.4;font-weight:600}
.hero h1 em{font-style:normal;color:var(--primary)}
.scena{display:grid;grid-template-columns:repeat(3,1fr);gap:calc(var(--spacing)*4);
  margin-top:calc(var(--spacing)*4)}
.scena div{border-left:2px solid var(--border);padding-left:calc(var(--spacing)*3)}
.scena b{display:block;font-size:10.5px;text-transform:uppercase;letter-spacing:.08em;
  color:var(--muted-foreground);margin-bottom:2px;font-weight:600}
.scena span{font-size:13px}

/* --- impianto a due colonne ---------------------------------------- */
.cols{display:grid;grid-template-columns:1fr 390px;gap:calc(var(--spacing)*4);align-items:start}

/* --- chat ----------------------------------------------------------- */
.chat{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);
  box-shadow:var(--shadow-sm);display:flex;flex-direction:column;height:660px}
.intestazione{display:flex;align-items:center;gap:calc(var(--spacing)*3);
  padding:calc(var(--spacing)*4) calc(var(--spacing)*5);border-bottom:1px solid var(--border)}
.pallino{width:8px;height:8px;border-radius:50%;background:var(--st-verde);flex:none}
.intestazione b{font-size:13px;font-weight:600}
/* la meta va a destra; il selettore deve essere specifico perche' anche
   .pallino e' uno <span> e con "intestazione span" finiva spinto pure lui,
   trascinando il titolo al centro */
.intestazione .meta{font-size:12px;color:var(--muted-foreground);margin-left:auto}
.flusso{flex:1;overflow-y:auto;padding:calc(var(--spacing)*5);
  display:flex;flex-direction:column;gap:calc(var(--spacing)*4)}
.msg{max-width:88%}
.msg.io{align-self:flex-end;background:var(--foreground);color:var(--background);
  padding:calc(var(--spacing)*3) calc(var(--spacing)*4);border-radius:var(--radius);
  border-bottom-right-radius:4px;font-size:14px}
.msg.bot{align-self:flex-start;width:100%}
.msg.bot .corpo{font-size:15px;line-height:1.8}
.pie{margin-top:calc(var(--spacing)*3);font-size:12px;color:var(--muted-foreground);
  display:flex;align-items:center;gap:calc(var(--spacing)*3);flex-wrap:wrap}
.pie kbd{font-family:var(--font-mono);font-size:10px;background:var(--muted);
  border:1px solid var(--border);border-radius:4px;padding:1px 5px}
/* --- tenuta della risposta: sotto la risposta, non sulla singola frase ---
   La confidenza di una frase e' un'informazione da approfondimento; quella
   che conta leggendo e' se la risposta nel suo insieme regge. Sta qui, con
   la composizione accanto: un totale che non si puo' scomporre e' proprio
   la cosa che questa demo denuncia. */
.tenuta{margin-top:calc(var(--spacing)*2);font-size:11px;color:var(--muted-foreground);
  display:flex;align-items:center;gap:7px;flex-wrap:wrap;row-gap:5px}
.tenuta .et{text-transform:uppercase;letter-spacing:.1em;font-size:10px}
.tenuta .liv{color:var(--secondary);font-weight:600;letter-spacing:.06em;font-size:10.5px}
.tenuta .comp{font-size:10.5px}
.tenuta .comp b{font-weight:600}
.tenuta .comp b[data-c=verde]{color:var(--st-verde)}
.tenuta .comp b[data-c=blu]{color:var(--st-blu)}
.tenuta .comp b[data-c=rosso]{color:var(--st-rosso)}
.tenuta .comp b[data-c=arancione]{color:var(--st-arancione)}
.avviso{background:var(--st-arancione-bg);border:1px solid #f0d4b6;border-radius:var(--radius);
  padding:calc(var(--spacing)*3) calc(var(--spacing)*4);font-size:12px;line-height:1.55;
  margin:calc(var(--spacing)*4) calc(var(--spacing)*5) 0}
.avviso b{color:var(--st-arancione)}
.pallino.spento{background:var(--st-arancione)}
.vuoto-chat{margin:auto;text-align:center;color:var(--muted-foreground);font-size:14px;
  line-height:1.7;padding:calc(var(--spacing)*6)}

/* --- frasi cliccabili ------------------------------------------------ */
.frase{cursor:pointer;border-bottom:1px solid #e9ebee;padding:1px 0;transition:.12s}
.frase:hover{background:var(--muted);border-bottom-color:var(--primary)}
.frase.sel{border-bottom:2px solid;padding-bottom:0}
/* mentre il giudice valuta: la frase c'e' gia' ma non ha ancora un verdetto.
   Nessun colore, perche' un colore provvisorio e' un'informazione falsa. */
.frase.attesa{border-bottom:1px dashed var(--muted-foreground);opacity:.65;
  animation:pulsa 1.4s ease-in-out infinite;cursor:default}
@keyframes pulsa{0%,100%{opacity:.5}50%{opacity:.85}}
.frase.sel[data-c=verde]{background:var(--st-verde-bg);border-color:var(--st-verde)}
.frase.sel[data-c=blu]{background:var(--st-blu-bg);border-color:var(--st-blu)}
.frase.sel[data-c=rosso]{background:var(--st-rosso-bg);border-color:var(--st-rosso)}
.frase.sel[data-c=arancione]{background:var(--st-arancione-bg);border-color:var(--st-arancione)}

/* --- suggerimenti + input -------------------------------------------- */
.sotto{border-top:1px solid var(--border);padding:calc(var(--spacing)*4) calc(var(--spacing)*5)}
.chips{display:flex;gap:calc(var(--spacing)*2);flex-wrap:wrap;margin-bottom:calc(var(--spacing)*3)}
.chip{background:var(--muted);border:1px solid var(--border);border-radius:999px;
  padding:calc(var(--spacing)*2) calc(var(--spacing)*3);font-family:inherit;font-size:11.5px;
  color:var(--muted-foreground);cursor:pointer;transition:.15s;max-width:100%;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.chip:hover{border-color:var(--primary);color:var(--foreground);background:var(--card)}
.riga{display:flex;gap:calc(var(--spacing)*2)}
.riga input{flex:1;font-family:inherit;font-size:14px;padding:calc(var(--spacing)*3) calc(var(--spacing)*4);
  border:1px solid var(--border);border-radius:var(--radius);background:var(--background);
  color:var(--foreground);outline:none;transition:.15s}
.riga input:focus{border-color:var(--primary)}
.riga button{background:var(--primary);color:var(--primary-foreground);border:none;
  border-radius:var(--radius);padding:0 calc(var(--spacing)*5);cursor:pointer;
  font-family:inherit;font-size:13px;font-weight:600}
.riga button:hover{filter:brightness(1.05)}
.puntini span{display:inline-block;width:5px;height:5px;border-radius:50%;
  background:var(--muted-foreground);margin-right:3px;animation:b 1.2s infinite}
.puntini span:nth-child(2){animation-delay:.15s}.puntini span:nth-child(3){animation-delay:.3s}
@keyframes b{0%,60%,100%{opacity:.25}30%{opacity:1}}

/* --- pannello verifica ------------------------------------------------ */
.pannello{position:sticky;top:calc(var(--spacing)*7)}
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);
  padding:calc(var(--spacing)*5);box-shadow:var(--shadow-sm)}
.titolo-p{font-size:10.5px;text-transform:uppercase;letter-spacing:.09em;font-weight:600;
  color:var(--muted-foreground);margin-bottom:calc(var(--spacing)*4)}
.attesa{font-size:13.5px;color:var(--muted-foreground);line-height:1.7}
.legenda{margin-top:calc(var(--spacing)*4);display:flex;flex-direction:column;gap:6px}
.lg{display:flex;gap:calc(var(--spacing)*2);align-items:baseline;font-size:11.5px}
.lg i{width:7px;height:7px;border-radius:50%;flex:none;transform:translateY(-1px)}
.lg b{font-weight:600;font-style:normal}
.lg span{color:var(--muted-foreground);font-size:12.5px}
.badge{display:inline-flex;font-size:10.5px;font-weight:600;text-transform:uppercase;
  letter-spacing:.07em;padding:3px 9px;border-radius:999px;color:#fff}
.badge[data-c=verde]{background:var(--st-verde)} .badge[data-c=blu]{background:var(--st-blu)}
.badge[data-c=rosso]{background:var(--st-rosso)} .badge[data-c=arancione]{background:var(--st-arancione)}
.conf{font-size:10.5px;color:var(--muted-foreground);margin-left:auto;
  text-transform:uppercase;letter-spacing:.1em}
.conf b{color:var(--secondary);font-weight:600}
/* i pallini da soli non dicono di cosa sono la misura: l'etichetta lo dice. */
.conf em{font-style:normal;margin-right:6px;letter-spacing:.08em}
.dato{color:var(--secondary);font-weight:600}
.testa{display:flex;align-items:center;gap:calc(var(--spacing)*2);margin-bottom:calc(var(--spacing)*4);flex-wrap:wrap;row-gap:6px}
.citata{font-size:13px;line-height:1.6;padding-left:calc(var(--spacing)*3);
  border-left:2px solid var(--border);margin-bottom:calc(var(--spacing)*3)}
.motivo{font-size:13px;color:var(--muted-foreground);margin-bottom:calc(var(--spacing)*4);line-height:1.65}
.sez{font-size:10px;text-transform:uppercase;letter-spacing:.09em;color:var(--muted-foreground);
  font-weight:600;margin-bottom:calc(var(--spacing)*2)}
.prova{font-family:var(--font-mono);font-size:11px;line-height:1.75;background:var(--muted);
  border-radius:calc(var(--radius)/1.5);padding:calc(var(--spacing)*3);
  max-height:210px;overflow:auto;white-space:pre-wrap;word-break:break-word}
.prova .ctx{color:#9aa1ab}
.prova mark{background:var(--st-verde-bg);color:var(--foreground);
  box-shadow:inset 0 -2px 0 var(--st-verde);padding:1px 0}
.prova mark[data-c=rosso]{background:var(--st-rosso-bg);box-shadow:inset 0 -2px 0 var(--st-rosso)}
.fonte{margin-top:calc(var(--spacing)*3);border-top:1px solid var(--border);
  padding-top:calc(var(--spacing)*3)}
.fonte-t{;font-size:12.5px;line-height:1.55;
  color:var(--foreground)}
.fonte-f{font-family:var(--font-mono);font-size:10px;color:var(--muted-foreground);
  margin-top:4px;word-break:break-all}
.blocco{margin-bottom:calc(var(--spacing)*4)}
.nota{font-size:12.5px;border-radius:calc(var(--radius)/1.5);padding:calc(var(--spacing)*3);
  line-height:1.6}
.nota.tempo{background:var(--st-arancione-bg);border:1px solid #f0d4b6}
.nota.scarto{background:var(--muted);border:1px solid var(--border);color:var(--muted-foreground)}
.tl{margin-top:calc(var(--spacing)*2);font-family:var(--font-mono);font-size:10.5px}
.tl div{display:flex;gap:calc(var(--spacing)*2);padding:3px 0;border-left:2px solid var(--st-arancione);
  padding-left:calc(var(--spacing)*3);margin-left:2px}
.tl b{color:var(--st-arancione);white-space:nowrap}
.tl span{color:var(--muted-foreground)}
.cuciti{font-size:11px;font-family:var(--font-mono);color:var(--muted-foreground);line-height:1.7}
.cuciti div{padding:2px 0;border-bottom:1px solid var(--border)}


/* --- fonte come chip, non come paragrafo (pattern Compass) ----------- */
.chip-f{font-family:var(--font-mono);font-size:9.5px;letter-spacing:.06em;text-transform:none;
  border:1px solid var(--border);border-radius:5px;padding:3px 8px;cursor:pointer;
  background:var(--card);color:var(--muted-foreground);transition:.15s;display:inline-block;
  max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;vertical-align:middle}
.chip-f:hover{border-color:var(--primary);color:var(--foreground)}
.chip-f.cucita{border-style:dashed}
.chip-riga{display:flex;gap:5px;flex-wrap:wrap;margin-top:6px}
.mini-leg{font-size:9.5px;color:var(--muted-foreground);text-transform:none;letter-spacing:0;
  margin-left:6px;font-weight:400}
/* pallini di confidenza al posto del numero */
.dots{display:inline-flex;gap:3px;margin-right:5px;vertical-align:1px}
.dots i{width:5px;height:5px;border-radius:50%;background:var(--border)}
.dots i.on{background:var(--secondary)}
/* prova cucita: tratteggio invece di pieno, la texture dice quanto e' diretta */
.prova mark.cucita{background:transparent;box-shadow:none;
  border-bottom:2px dashed var(--st-blu)}

/* --- popup di approfondimento ---------------------------------------- */
.velo{position:fixed;inset:0;background:rgba(17,24,39,.45);display:flex;align-items:center;
  justify-content:center;z-index:50;padding:calc(var(--spacing)*6)}
.velo[hidden]{display:none}
.finestra{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);
  box-shadow:var(--shadow-lg);max-width:860px;width:100%;max-height:88vh;
  display:flex;flex-direction:column}
.f-testa{display:flex;align-items:flex-start;gap:calc(var(--spacing)*3);
  padding:calc(var(--spacing)*4) calc(var(--spacing)*5);border-bottom:1px solid var(--border)}
.f-testa h3{font-size:13px;font-weight:600;margin-bottom:3px}
.f-testa p{font-size:11px;color:var(--muted-foreground);line-height:1.5}
.f-x{margin-left:auto;background:none;border:1px solid var(--border);border-radius:6px;
  width:26px;height:26px;cursor:pointer;color:var(--muted-foreground);font-family:inherit;flex:none}
.f-x:hover{border-color:var(--primary);color:var(--foreground)}
.f-corpo{overflow:auto;padding:calc(var(--spacing)*5);font-family:var(--font-mono);
  font-size:11.5px;line-height:1.8;white-space:pre-wrap;word-break:break-word}
.f-corpo mark{background:var(--st-verde-bg);box-shadow:inset 0 -2px 0 var(--st-verde);
  padding:2px 0;scroll-margin:120px}
.f-corpo mark[data-c=rosso]{background:var(--st-rosso-bg);box-shadow:inset 0 -2px 0 var(--st-rosso)}
.f-corpo mark[data-c=blu]{background:var(--st-blu-bg);box-shadow:inset 0 -2px 0 var(--st-blu)}
.f-pie{border-top:1px solid var(--border);padding:calc(var(--spacing)*3) calc(var(--spacing)*5);
  font-family:var(--font-mono);font-size:10px;color:var(--muted-foreground)}

/* --- materiale d'archivio e riferimenti: monospace di sistema --------- */
.msg.io,.msg.bot .corpo,.prova,.f-corpo,.chip-f,.fonte-f,.f-pie,.tl,.cuciti,.dove{
  font-family:var(--font-sans)}
.piede{margin-top:calc(var(--spacing)*5);font-size:12.5px;color:var(--muted-foreground);
  text-align:center;line-height:1.75;
  max-width:840px;margin-left:auto;margin-right:auto}
@media(max-width:980px){.cols{grid-template-columns:1fr}.pannello{position:static}
  .scena{grid-template-columns:1fr}.chat{height:auto;min-height:520px}}
"""

JS = """
const CASI=DATI.casi; let sel=null, casoSel=null, inCorso=false;
const $=s=>document.querySelector(s);
const esc=t=>t.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const norm=t=>t.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
const VUOTE=new Set(['il','lo','la','i','gli','le','un','una','di','a','da','in','con','su',
 'per','del','della','dei','delle','che','e','ed','o','ma','se','non','si','sono','come',
 'qual','quale','quanto','quanti','chi','cosa','ha','hanno','al','alla','dell','all','e2']);
const parole=t=>norm(t).split(/[^a-z0-9]+/).filter(w=>w.length>2&&!VUOTE.has(w));

// Match a parole con la domanda precalcolata piu' vicina. E' una demo statica:
// meglio ammettere di non avere la risposta che costruirne una finta.
function cerca(q){
  const pq=parole(q); if(!pq.length) return null;
  let best=null,bs=0;
  CASI.forEach((c,i)=>{
    const pc=new Set(parole(c.domanda));
    const comuni=pq.filter(w=>pc.has(w)).length;
    const s=comuni/Math.max(pq.length,1);
    if(s>bs){bs=s;best=i}
  });
  return bs>=0.45?best:null;
}

function scrolla(){const f=$('#flusso');f.scrollTop=f.scrollHeight}

function bolla(testo){
  const d=document.createElement('div');
  d.className='msg io'; d.textContent=testo;
  $('#flusso').appendChild(d); scrolla();
}

function scrivendo(){
  const d=document.createElement('div');
  d.className='msg bot'; d.id='typing';
  d.innerHTML='<div class="puntini"><span></span><span></span><span></span></div>';
  $('#flusso').appendChild(d); scrolla();
}

// I pallini servono in due posti, quindi vivono qui e non dentro un solo
// riquadro.
const dots=n=>{let o='<span class="dots">';for(let k=0;k<4;k++)o+=`<i class="${k<n?'on':''}"></i>`;return o+'</span>'};

// La confidenza non sta piu' sulla singola frase: sta sulla risposta, che e'
// l'unita' che una persona legge e decide se usare.
//
// E non e' la media dei numeri che il giudice dichiara su se stesso: quelli
// dicono quanto e' sicuro del proprio verdetto, non quanto regge la risposta —
// un "fuori corpus" molto sicuro alzerebbe la media invece di abbassarla.
// Qui pesano i verdetti, che sono la cosa che il sistema misura davvero, e la
// composizione resta accanto al totale: un numero che non si puo' scomporre e'
// esattamente cio' che questa demo denuncia.
const PESO={ripescato:1, inferito:.6, fuori_corpus:.15, non_supportato:0};
const NOME_STATO={ripescato:'ripescate', inferito:'inferite',
                  non_supportato:'non supportate', fuori_corpus:'fuori corpus'};
const COLORE_STATO={ripescato:'verde', inferito:'blu',
                    non_supportato:'rosso', fuori_corpus:'arancione'};

function tenuta(c){
  const fatte=(c.affermazioni||[]).filter(a=>a.stato&&a.stato!=='non_verificata');
  if(!fatte.length) return null;
  let v=fatte.reduce((s,a)=>s+(PESO[a.stato]??.5),0)/fatte.length;
  // Un'affermazione smentita non si compensa con due verdi: la risposta
  // contiene comunque qualcosa che l'archivio nega, e va detto.
  if(fatte.some(a=>a.stato==='non_supportato')) v=Math.min(v,.45);
  return {liv: v>=.9?['ALTA',4]:v>=.6?['MEDIA',3]:v>=.3?['BASSA',2]:['MINIMA',1],
          conteggi: Object.keys(PESO).map(s=>[s,fatte.filter(a=>a.stato===s).length])
                          .filter(([,n])=>n),
          fatte: fatte.length, tot: (c.affermazioni||[]).length};
}

function rigaTenuta(c){
  const t=tenuta(c);
  if(!t) return '<span class="et">tenuta della risposta</span> in verifica…';
  const parti=t.conteggi.map(([s,n])=>
    `<b data-c="${COLORE_STATO[s]}">${n}</b> ${NOME_STATO[s]}`).join(' \u00b7 ');
  const restanti=t.tot-t.fatte;
  // Un totale calcolato su meta' dei verdetti puo' crollare quando arrivano gli
  // altri. Mostrarlo va bene — nasconderlo sarebbe peggio — ma deve dire di
  // essere provvisorio, o la prima lettura resta quella sbagliata.
  return `<span class="et">tenuta ${restanti?'provvisoria':'della risposta'}</span>${dots(t.liv[1])}`
    +`<b class="liv">${t.liv[0]}</b>`
    +`<span class="comp">${parti}${restanti?` \u00b7 ${restanti} in verifica`:''}</span>`;
}

function aggiornaTenuta(ci){
  const el=document.querySelector(`.tenuta[data-ci="${ci}"]`);
  if(el) el.innerHTML=rigaTenuta(CASI[ci]);
}

function rispostaBot(i){
  document.getElementById('typing')?.remove();
  const c=CASI[i];
  let resto=c.risposta, out=[];
  c.affermazioni.forEach((a,k)=>{
    const idx=resto.indexOf(a.testo); if(idx<0) return;
    out.push(esc(resto.slice(0,idx)));
    const inAttesa=!a.stato;
    out.push(`<span class="frase${inAttesa?' attesa':''}" data-ci="${i}" data-ai="${k}"`
      +` data-c="${a.colore||''}"${inAttesa?'':` onclick="apri(${i},${k},this)"`}>${esc(a.testo)}</span>`);
    resto=resto.slice(idx+a.testo.length);
  });
  out.push(esc(resto));
  const d=document.createElement('div');
  d.className='msg bot';
  d.innerHTML=`<div class="corpo">${out.join('')}</div>
    <div class="pie"><kbd>clicca una frase</kbd> per vedere su cosa poggia ·
    <span class="dato">${c.affermazioni.length}</span> affermazioni ·
    <span class="dato">${c.passaggi_recuperati.length}</span> passaggi recuperati</div>
    <div class="tenuta" data-ci="${i}">${rigaTenuta(c)}</div>`;
  $('#flusso').appendChild(d); scrolla();
}

function nonSo(){
  document.getElementById('typing')?.remove();
  const d=document.createElement('div');
  d.className='msg bot';
  d.innerHTML=`<div class="corpo" style="color:var(--muted-foreground);font-size:14px">
    Questa è una demo statica: le risposte precalcolate sono quattro, e per questa
    domanda non ne ho una. Nella versione collegata all'API la domanda partirebbe
    davvero verso l'archivio.<br><br>Prova con uno dei suggerimenti qui sotto.</div>`;
  $('#flusso').appendChild(d); scrolla();
}

// L'endpoint live non e' ancora pubblicato: finche' API_ATTIVA resta false la
// chat usa solo le risposte precalcolate. Il percorso di discesa pero' e' gia'
// cablato e ispezionabile, cosi' quando l'endpoint arriva non c'e' da inventare
// il comportamento sotto pressione: al primo 402 o 429 si passa allo statico e
// lo si dichiara, invece di mostrare un errore o restare a girare a vuoto.
// L'endpoint e' pubblicato: la chat interroga l'archivio davvero. Se manca la
// chiave, se il budget finisce o se la funzione non risponde, si scende alle
// quattro risposte precalcolate dicendolo.
const API_ATTIVA=true;
let statico=false;

function passaAStatico(motivo){
  if(statico) return; statico=true;
  document.querySelector('.pallino')?.classList.add('spento');
  const d=document.createElement('div');
  d.className='avviso';
  d.innerHTML=`<b>Budget della demo esaurito${motivo?' — '+esc(motivo):''}.</b>
    Da qui in avanti rispondo solo con le quattro risposte gia' calcolate: quelle
    restano vere e verificate, ma le domande nuove non partono piu' verso l'archivio.`;
  $('#flusso').before(d);
}

// Lo stesso taglio in affermazioni che fa il verificatore lato server: righe
// di elenco e di tabella valgono una affermazione, il resto va a frasi.
function spezza(testo){
  const fuori=[];
  // regex invece di '\\n' in una stringa: l'escaping fra Python e JS
  // aveva prodotto una vera andata a capo dentro una stringa, cioe' un
  // errore di sintassi che faceva fallire l'intero script
  testo.split(/[\\r\\n]+/).forEach(riga=>{
    riga=riga.trim(); if(!riga) return;
    if(/^([-*\u2022]|\d+[.)]|\|)/.test(riga)){fuori.push(riga.replace(/^[-*\u2022]/,'').trim());return}
    riga.split(/(?<=[.!?])\s+(?=[A-ZÀÈÉÌÒÙ0-9])/).forEach(f=>{
      f=f.trim(); if(f.length>15) fuori.push(f);
    });
  });
  return fuori;
}

// Ogni frase ha la sua richiesta, lanciate insieme: l'utente vede i verdetti
// arrivare uno alla volta invece di aspettare che siano pronti tutti.
async function verificaFrase(ci,ai){
  const c=CASI[ci], a=c.affermazioni[ai];
  try{
    const r=await fetch('/api/verify',{method:'POST',
      headers:{'content-type':'application/json'},
      body:JSON.stringify({frase:a.testo, chunk_ids:c.chunk_ids})});
    if(r.status===402){passaAStatico('credito finito');return}
    if(!r.ok) throw new Error('HTTP '+r.status);
    const v=await r.json();
    if(v.esaurito){passaAStatico(v.motivo);return}
    if(v.errore) throw new Error(v.errore);
    Object.assign(a, v);
  }catch(e){
    a.stato='non_verificata'; a.colore='grigio';
    a.motivo='Verifica non riuscita: '+e.message; a.confidenza=0;
  }
  const el=document.querySelector(`.frase[data-ci="${ci}"][data-ai="${ai}"]`);
  if(el){el.classList.remove('attesa'); el.dataset.c=a.colore;
         el.onclick=()=>apri(ci,ai,el)}
  aggiornaTenuta(ci);
  if(sel===ai&&casoSel===ci) pannello();
}

async function chiediAllApi(q){
  const r=await fetch('/api/chat',{method:'POST',
    headers:{'content-type':'application/json'},body:JSON.stringify({domanda:q})});
  if(r.status===402||r.status===429){passaAStatico(r.status===402?'credito finito':'troppe richieste');return null}
  if(!r.ok) throw new Error('HTTP '+r.status);
  const dati=await r.json();
  if(dati.esaurito){passaAStatico(dati.motivo);return null}
  return dati;
}

async function invia(testo){
  if(inCorso) return;
  const q=(testo??$('#campo').value).trim(); if(!q) return;
  $('#campo').value=''; $('#vuotoChat')?.remove();
  inCorso=true; bolla(q); scrivendo();

  if(API_ATTIVA&&!statico){
    try{
      const vivo=await chiediAllApi(q);
      if(vivo){
        vivo.affermazioni=spezza(vivo.risposta).map(t=>({testo:t}));
        CASI.push(vivo);
        const ci=CASI.length-1;
        rispostaBot(ci);
        inCorso=false;
        vivo.affermazioni.forEach((_,k)=>verificaFrase(ci,k));
        return;
      }
    }catch(e){
      // un guasto vero non e' un budget finito: lo si dice com'e'
      document.getElementById('typing')?.remove();
      const d=document.createElement('div'); d.className='msg bot';
      d.innerHTML=`<div class="corpo" style="color:var(--st-rosso)">L'archivio non risponde (${esc(e.message)}).</div>`;
      $('#flusso').appendChild(d); inCorso=false; return;
    }
  }
  const i=cerca(q);
  setTimeout(()=>{ i===null?nonSo():rispostaBot(i); inCorso=false; }, 620);
}

function apri(ci,ai,el){
  document.querySelectorAll('.frase').forEach(f=>f.classList.remove('sel'));
  el.classList.add('sel'); casoSel=ci; sel=ai; pannello();
}

// I chip dicevano tutti "FONTE": una parola che non distingue una fonte
// dall'altra, cioe' l'unica cosa che dovevano fare. Il primo gettone diventa
// il nome del file, e dopo viene cio' che lo restringe — il numero del thread
// o la data — quando c'e'. Il percorso completo resta nel titolo e nel popup:
// il chip serve a riconoscere, non a descrivere.
// le citazioni scrivono la data in due modi — "12 novembre" e "23 ott" —
// quindi il ritaglio accetta sia il mese per esteso sia l'abbreviazione.
const MESI_IT=/(\d{1,2})\s+(gen|feb|mar|apr|mag|giu|lug|ago|set|ott|nov|dic)[a-z]*/i;
function etichettaFonte(citation,file){
  const pezzi=[];
  const nome=(file||'').split('/').pop();
  if(nome) pezzi.push(nome);
  const c=citation||'';
  const th=c.match(/Thread #(\d+)/);
  if(th) pezzi.push('#'+th[1]);
  const dt=c.match(MESI_IT);
  if(dt) pezzi.push(dt[1]+' '+dt[2].toLowerCase());
  return pezzi.join(' \u00b7 ')||'FONTE';
}

function pannello(){
  const p=$('#pannello');
  if(sel===null){
    p.innerHTML=`<div class="card"><div class="titolo-p">Verifica</div>
      <div class="attesa">Ogni risposta viene smontata frase per frase e confrontata
      con l'archivio da un secondo modello, che non sa come è stata prodotta.
      Clicca una frase per vedere il verdetto e la prova.</div>
      <div class="legenda">
        <div class="lg"><i style="background:var(--st-verde)"></i><b>Ripescato</b>
          <span>— un passaggio lo dice alla lettera</span></div>
        <div class="lg"><i style="background:var(--st-blu)"></i><b>Inferito</b>
          <span>— regge, ma cucito da più fonti</span></div>
        <div class="lg"><i style="background:var(--st-rosso)"></i><b>Non supportato</b>
          <span>— l'archivio dice altro</span></div>
        <div class="lg"><i style="background:var(--st-arancione)"></i><b>Fuori corpus</b>
          <span>— l'archivio non ne parla</span></div>
      </div></div>`;
    return;
  }
  const a=CASI[casoSel].affermazioni[sel];
  let h=`<div class="card"><div class="testa">
    <span class="badge" data-c="${a.colore}">${a.stato.replace('_',' ')}</span></div>
    <div class="citata">${esc(a.testo)}</div>
    <div class="motivo">${esc(a.motivo)}</div>`;

  if(a.ancora){
    const k=a.ancora.contesto||{};
    const cucita=a.colore==='blu';
    h+=`<div class="blocco"><div class="sez">La prova
        <span class="mini-leg">${cucita?'segnale cucito':'frammento letterale'}</span></div>
      <div class="prova"><span class="ctx">${esc(k.prima||'')}</span><mark data-c="${a.colore}" class="${cucita?'cucita':''}">${esc(k.prova||a.ancora.citazione)}</mark><span class="ctx">${esc(k.dopo||'')}</span></div>
      <div class="chip-riga"><button class="chip-f" onclick="apriFonte(${casoSel},${sel})"
        title="${esc(a.ancora.dove)}">${esc(etichettaFonte(a.ancora.dove,a.ancora.file))} ↗</button></div></div>`;
  }
  if(a.conflitto){
    h+=`<div class="blocco"><div class="nota tempo"><b>L'archivio è cambiato nel tempo.</b><br>
      ${esc(a.conflitto.nota)}<div class="tl">
      <div><b>${esc((a.conflitto.prima.quando||'').slice(0,10))}</b><span>${esc((a.conflitto.prima.dove||'').split('>')[0])}</span></div>
      <div><b>${esc((a.conflitto.dopo.quando||'').slice(0,10))}</b><span>${esc((a.conflitto.dopo.dove||'').split('>')[0])}</span></div>
      </div></div></div>`;
  }
  if(a.ancora_scartata){
    h+=`<div class="blocco"><div class="nota scarto"><b>Prova scartata dal revisore.</b><br>
      ${esc(a.ancora_scartata.split(' — ').pop())}</div></div>`;
  }
  // la fonte gia' esibita sopra non si ripete qui sotto
  const altre=(a.passaggi||[]).filter(x=>!a.ancora||x.chunk_id!==a.ancora.chunk_id);
  if(altre.length){
    h+=`<div class="blocco"><div class="sez">${a.ancora?'Altre fonti':'Fonti'}
        <span class="mini-leg">${a.ancora?'':'nessuna lo dice alla lettera'}</span></div>
      <div class="chip-riga">${altre.map((x,j)=>
        `<button class="chip-f cucita" onclick="apriPassaggio(${casoSel},${sel},${a.passaggi.indexOf(x)})"
          title="${esc(x.citation)}">${esc(etichettaFonte(x.citation,x.file))} ↗</button>`).join('')}</div></div>`;
  }
  p.innerHTML=h+'</div>';
}

// I suggerimenti si legano con un listener, non con onclick inline: la domanda
// contiene apostrofi e virgolette che dentro un attributo HTML spezzano tutto.

// --- approfondimento: apre il canale per intero ------------------------
// Il popup non mostra la finestrella che ho deciso io: apre il file, ci
// scorre dentro fino al passaggio e lo evidenzia. Chi vuole leggere cosa
// c'era prima e cosa e' successo dopo puo' farlo senza chiedere permesso.
function mostraFile(file, inizio, fine, colore, titolo, sotto){
  const testo=DATI.sorgenti[file];
  if(!testo){alert('Sorgente non incorporata: '+file);return}
  const pre=esc(testo.slice(0,inizio)), mid=esc(testo.slice(inizio,fine)), post=esc(testo.slice(fine));
  $('#velo').hidden=false;
  $('#f-titolo').textContent=titolo;
  $('#f-sotto').textContent=sotto;
  $('#f-pie').textContent=`${file} · caratteri ${inizio}–${fine} · ${testo.length} in tutto`;
  $('#f-corpo').innerHTML=pre+`<mark id="qui" data-c="${colore}">${mid}</mark>`+post;
  document.getElementById('qui')?.scrollIntoView({block:'center'});
}
function apriFonte(ci,ai){
  const a=CASI[ci].affermazioni[ai], n=a.ancora;
  mostraFile(n.file, n.inizio, n.fine, a.colore, n.chip||'Fonte', n.dove);
}
function apriPassaggio(ci,ai,j){
  const a=CASI[ci].affermazioni[ai], x=a.passaggi[j];
  if(x.start==null){alert('Coordinate non disponibili per questo passaggio');return}
  mostraFile(x.file, x.start, x.end, 'blu', x.chip||'Fonte', x.citation);
}
function chiudi(){$('#velo').hidden=true}
document.addEventListener('keydown',e=>{if(e.key==='Escape')chiudi()});

$('#chips').innerHTML=CASI.map((c,i)=>
  `<button class="chip" data-i="${i}">${esc(c.domanda)}</button>`).join('');
document.querySelectorAll('.chip').forEach(b=>
  b.addEventListener('click',()=>invia(CASI[+b.dataset.i].domanda)));
$('#campo').addEventListener('keydown',e=>{if(e.key==='Enter')invia()});
pannello();
"""


def main() -> int:
    dati = json.loads(DATI.read_text(encoding="utf-8"))
    info = dati["indice"]
    html = f"""<!doctype html>
<html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Prometeo Cup — chiedi all'archivio</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>:root{{{TOKENS}}}{CSS}</style></head>
<body><div class="wrap">

<div class="hero">
  <div class="eyebrow">Prometeo Cup · archivio di progetto</div>
  <h1>Le citazioni ti dicono da dove viene una risposta.
      Non ti dicono <em>se quella frase regge davvero</em>.</h1>
  <div class="scena">
    <div><b>Cos'è</b><span>Sette mesi di email, riunioni, telefonate e chat sull'organizzazione
      di una partita di calcio fra robot: {info['chunks']} frammenti indicizzati.</span></div>
    <div><b>Cosa puoi fare</b><span>Chiedi quello che vuoi all'archivio, come faresti
      con qualsiasi assistente.</span></div>
    <div><b>La differenza</b><span>Clicca una frase della risposta: il sistema dice se
      l'archivio la sostiene, la smentisce, o non ne parla.</span></div>
  </div>
</div>

<div class="cols">
  <div class="chat">
    <div class="intestazione"><span class="pallino"></span>
      <b>Archivio Prometeo Cup</b>
      <span class="meta"><b class="dato">{info['chunks']}</b> frammenti · <b class="dato">6</b> canali</span></div>
    <div class="flusso" id="flusso">
      <div class="vuoto-chat" id="vuotoChat">
        Chiedi qualcosa sull'evento.<br>Se non sai da dove partire, usa un suggerimento.
      </div>
    </div>
    <div class="sotto">
      <div class="chips" id="chips"></div>
      <div class="riga">
        <input id="campo" autocomplete="off" placeholder="Scrivi una domanda sull'archivio…">
        <button onclick="invia()">Invia</button>
      </div>
    </div>
  </div>
  <div class="pannello" id="pannello"></div>
</div>

<div class="piede">
  Risposte generate con Claude sui {info['chunks']} frammenti indicizzati con
  {info['model']}, verificate frase per frase da un secondo modello che non sa come
  sono state prodotte. Nessun contenuto è scritto a mano: verdetti, citazioni e offset
  vengono da esecuzioni reali.<br>
  La chat interroga l'archivio dal vivo. Raggiunto il tetto di spesa restano quattro
  risposte precalcolate, e la chat lo dichiara invece di fingere. Lo stato arancione segna
  le domande a cui l'archivio non risponde: chi risponde lo ammette invece di riempire il vuoto.
</div>


<div class="velo" id="velo" hidden onclick="if(event.target===this)chiudi()">
  <div class="finestra">
    <div class="f-testa">
      <div><h3 id="f-titolo"></h3><p id="f-sotto"></p></div>
      <button class="f-x" onclick="chiudi()">✕</button>
    </div>
    <div class="f-corpo" id="f-corpo"></div>
    <div class="f-pie" id="f-pie"></div>
  </div>
</div>

</div>
<script>const DATI={json.dumps(dati, ensure_ascii=False)};\n{JS}</script>
</body></html>"""
    USCITA.write_text(html, encoding="utf-8")
    print(f"scritto {USCITA} ({USCITA.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
