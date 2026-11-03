"""Genera le pagine HTML 9:16 di un'uscita della Gazzetta del Dragone.

Uso: python template/genera_uscita.py contenuti/giornata_07.py

Il file dei contenuti definisce un dizionario USCITA (vedi contenuti/esempio.py).
Le pagine finiscono in uscite/<cartella>/, insieme al file .md con i testi
puliti per Humanizer.
"""
import base64
import html
import importlib.util
import mimetypes
import os
import re
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RADICE, "assets", "logo"))
import genera_logo as logo  # noqa: E402

NAVY = logo.NAVY
CIANO = logo.CIANO
# Rosa della maglia del portiere: colore della rubrica di Zanni, al posto del ciano.
ROSA = "#EC78C0"
FIRMA = "© Redazione La Gazzetta del Dragone, tutti i diritti riservati"
COND = "'Franklin Gothic Demi Cond', 'Franklin Gothic Medium Cond', Impact, 'Arial Narrow', sans-serif"
BAST = "'Franklin Gothic Demi', 'Franklin Gothic Medium', Arial, sans-serif"
# Nelle storie Instagram la barra del profilo (in alto) e il campo di risposta
# (in basso) coprono circa 250 px: lì non va niente da leggere, firma compresa.
ZONA_ALTO = 250
ZONA_BASSO = 250
# Nessun testo sotto i 24 px: sul telefono la pagina si vede larga circa 390 px.
# Inizio del contenuto sotto la testata: ridotta (interne) e grande (prima pagina).
TOP_INT = ZONA_ALTO + 130
TOP_COP = ZONA_ALTO + 350

CSS = f"""
@page {{ size: 1080px 1920px; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 1080px; height: 1920px; background: #fff; }}
body {{
  color: {NAVY};
  font-family: Georgia, 'Times New Roman', serif;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}}
.pagina {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; padding: {ZONA_ALTO}px 56px 0 40px; }}
.filigrana {{ position: absolute; right: -120px; bottom: 120px; width: 760px; opacity: .045; pointer-events: none; }}
.lato {{
  position: absolute; right: 10px; top: 50%; transform: translateY(-50%) rotate(90deg);
  transform-origin: center; white-space: nowrap; font-size: 24px; letter-spacing: 2px;
  text-transform: uppercase; opacity: .7; width: 0; display: flex; justify-content: center;
}}
.testata svg {{ display: block; width: 1000px; height: auto; }}
.dataline {{
  display: flex; justify-content: space-between; font-size: 26px; letter-spacing: 2px;
  text-transform: uppercase; padding: 10px 0 0;
}}
.contenuto {{ position: absolute; left: 40px; right: 56px; top: var(--top); bottom: {ZONA_BASSO + 100}px; overflow: hidden; }}
.titoli {{ font-family: 'Franklin Gothic Demi', 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif; }}
.gioco {{ background: {CIANO}; color: {NAVY}; padding: 0 14px; -webkit-box-decoration-break: clone; box-decoration-break: clone; }}
/* Prima pagina: sopratitolo, titolone, catenaccio, apertura con foto e spalla,
   taglio basso con i richiami alle pagine interne. */
.cop {{ height: 100%; display: flex; flex-direction: column; }}
.sopra {{ display: flex; align-items: stretch; border-top: 6px solid {NAVY}; border-bottom: 2px solid {NAVY}; margin-top: 14px; }}
.sopra .kicker {{ background: {CIANO}; padding: 8px 16px; font-size: 26px; letter-spacing: 2px; text-transform: uppercase; white-space: nowrap; display: flex; align-items: center; }}
.sopra .testo-sopra {{ padding: 8px 16px; font-size: 28px; line-height: 1.2; font-weight: 700; display: flex; align-items: center; }}
.titolone {{
  font-family: 'Franklin Gothic Demi Cond', 'Franklin Gothic Medium Cond', Impact, 'Arial Narrow', sans-serif;
  font-weight: 400; font-size: 220px; line-height: 1; letter-spacing: -1px; text-transform: uppercase;
  margin: 28px 0 20px; white-space: normal; overflow-wrap: normal;
}}
.titolone .gioco {{ padding: 0 12px; line-height: 1; }}
.catenaccio {{ font-size: 32px; line-height: 1.22; font-weight: 700; margin-bottom: 12px; }}
.rimando {{ font-family: 'Franklin Gothic Demi', Arial, sans-serif; font-weight: 700; font-size: .7em; letter-spacing: 1px; text-transform: uppercase; white-space: nowrap; }}
.rimando::before {{ content: "▸ "; }}
.apertura {{ flex: 1 0 auto; min-height: 340px; display: grid; grid-template-columns: 1fr 320px; gap: 22px; border-top: 2px solid {NAVY}; padding-top: 16px; }}
.foto {{ position: relative; background: {CIANO}; overflow: hidden; display: flex; align-items: center; justify-content: center; }}
.foto img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.foto .segnaposto {{ font-size: 24px; letter-spacing: 3px; text-transform: uppercase; }}
.foto figcaption {{ position: absolute; left: 0; right: 0; bottom: 0; background: rgba(255,255,255,.92); padding: 8px 14px; font-size: 26px; line-height: 1.25; font-style: italic; }}
.punteggio {{ position: absolute; left: 0; top: 0; background: {NAVY}; color: #fff; padding: 10px 18px; display: flex; gap: 14px; align-items: center; font-size: 26px; text-transform: uppercase; letter-spacing: 1px; }}
.punteggio b {{ font-family: 'Franklin Gothic Demi Cond', Impact, sans-serif; font-weight: 400; font-size: 64px; line-height: 1; letter-spacing: 0; }}
.spalla {{ display: flex; flex-direction: column; gap: 14px; }}
.blocco {{ border-top: 6px solid {CIANO}; font-size: 26px; line-height: 1.25; }}
.blocco h3 {{ font-family: 'Franklin Gothic Demi', Arial, sans-serif; font-weight: 700; font-size: 24px; letter-spacing: 2px; text-transform: uppercase; padding: 6px 0 4px; }}
.blocco .grande {{ font-family: 'Franklin Gothic Demi Cond', Impact, sans-serif; font-size: 76px; line-height: .95; display: block; }}
.mini {{ width: 100%; border-collapse: collapse; font-size: 26px; }}
.mini td {{ padding: 4px 0; border-bottom: 1px solid {NAVY}; }}
.mini td:last-child {{ text-align: right; }}
.mini tr.nostra td {{ background: {CIANO}; }}
.richiami {{ display: grid; grid-template-columns: repeat(3, 1fr); margin-top: 16px; border-top: 6px solid {NAVY}; }}
.richiami > div {{ padding: 12px 18px 0 0; }}
.richiami > div + div {{ border-left: 1px solid {NAVY}; padding-left: 18px; }}
.richiami .occ {{ display: inline-block; background: {CIANO}; padding: 3px 10px; font-size: 24px; letter-spacing: 2px; text-transform: uppercase; }}
.richiami h4 {{ font-family: 'Franklin Gothic Demi', Arial, sans-serif; font-weight: 700; font-size: 34px; line-height: 1.08; margin: 8px 0 6px; }}
.richiami .di {{ display: block; font-family: {BAST}; font-weight: 700; font-size: 24px; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 6px; }}
.richiami .rimando {{ font-size: 24px; }}
/* Pagine interne: testatina con numero di pagina e sezione, occhiello, titolo
   in condensato, catenaccio, firma, testo a una colonna, box dei numeri. */
.int {{ height: 100%; display: flex; flex-direction: column; }}
.folio {{ display: flex; align-items: stretch; height: 58px; border-bottom: 3px solid {NAVY}; margin-top: 4px; flex: none; }}
.folio .pg {{ background: {NAVY}; color: #fff; font-family: {COND}; font-size: 46px; width: 100px; display: flex; align-items: center; justify-content: center; }}
.folio .sez {{ background: {CIANO}; padding: 0 22px; font-size: 24px; letter-spacing: 3px; text-transform: uppercase; display: flex; align-items: center; }}
.folio .info {{ margin-left: auto; display: flex; align-items: center; font-size: 24px; letter-spacing: 1px; text-transform: uppercase; }}
.occhiello {{ align-self: flex-start; background: {CIANO}; padding: 6px 16px; font-size: 24px; letter-spacing: 3px; text-transform: uppercase; margin: 24px 0 12px; }}
.titolo {{ font-family: {COND}; font-weight: 400; font-size: 104px; line-height: 1; letter-spacing: -1px; margin-bottom: 14px; }}
.titolo .gioco {{ padding: 0 10px; }}
.cat-int {{ font-size: 34px; line-height: 1.22; font-weight: 700; margin-bottom: 14px; }}
.byline {{ display: flex; justify-content: space-between; align-items: center; border-top: 1px solid {NAVY}; border-bottom: 4px solid {NAVY}; padding: 10px 0; font-size: 24px; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 20px; flex: none; }}
.byline.autore {{ padding: 6px 0 8px; }}
.byline .nome {{ font-family: {COND}; font-weight: 400; font-size: 42px; letter-spacing: 0; text-transform: none; background: {CIANO}; padding: 0 10px; margin-left: 6px; }}
.foto-int {{ height: 380px; margin-bottom: 24px; flex: none; }}
.tab-int {{ display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 6px 26px; background: {NAVY}; color: #fff; padding: 10px 22px 12px; margin-bottom: 20px; font-size: 30px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }}
.tab-int .c {{ text-align: right; }}
.tab-int b {{ font-family: {COND}; font-weight: 400; font-size: 72px; line-height: 1; letter-spacing: 0; }}
.tab-int .mar {{ grid-column: 1 / -1; border-top: 1px solid {CIANO}; padding-top: 8px; font-size: 26px; font-weight: 400; font-style: italic; text-transform: none; letter-spacing: 0; }}
.colonne p {{ font-size: 34px; line-height: 1.45; margin-bottom: 16px; }}
.colonne p:first-child::first-letter {{ font-family: {COND}; float: left; font-size: 150px; line-height: .8; padding: 8px 14px 0 0; }}
.colonne p:last-of-type::after {{ content: " \\25A0"; font-size: .6em; }}
.cit {{ break-inside: avoid; border-top: 6px solid {CIANO}; border-bottom: 1px solid {NAVY}; padding: 14px 0 16px; margin: 4px 0 20px; font-size: 40px; line-height: 1.2; font-style: italic; font-weight: 700; }}
.cit cite {{ display: block; font-style: normal; font-weight: 400; font-size: 24px; letter-spacing: 2px; text-transform: uppercase; margin-top: 10px; }}
.segue {{ text-align: right; margin-top: 6px; font-size: 26px; }}
.seguito {{ display: flex; justify-content: space-between; align-items: baseline; gap: 20px; border-bottom: 4px solid {NAVY}; padding: 18px 0 10px; margin-bottom: 20px; }}
.titolo-seguito {{ font-family: {COND}; font-size: 48px; line-height: 1.05; }}
.seguito .segue {{ margin: 0; white-space: nowrap; }}
.cifre {{ margin-top: auto; display: grid; border-top: 6px solid {NAVY}; flex: none; }}
.cifre.alto {{ margin: 0 0 18px; }}
.cifre.alto .v {{ font-size: 52px; }}
.folio + .titolo {{ margin-top: 18px; }}
.gara:last-child {{ border-bottom: 0; padding-bottom: 0; }}
.cifre > div {{ padding: 12px 16px 0 0; font-size: 24px; line-height: 1.25; }}
.cifre > div + div {{ border-left: 1px solid {NAVY}; padding-left: 16px; }}
.cifre .k {{ display: inline-block; background: {CIANO}; padding: 2px 8px; font-size: 24px; letter-spacing: 1px; text-transform: uppercase; }}
.cifre .v {{ display: block; font-family: {COND}; font-size: 76px; line-height: 1; margin: 6px 0 2px; }}
table.dati {{ width: 100%; border-collapse: collapse; font-size: 28px; }}
table.dati th {{ font-family: {BAST}; font-weight: 700; text-align: center; padding: 10px 6px; background: {NAVY}; color: #fff; font-size: 24px; letter-spacing: 1px; }}
table.dati td {{ text-align: center; padding: 3px 6px; border-bottom: 1px solid {NAVY}; }}
table.dati td.sq, table.dati th.sq {{ text-align: left; }}
table.dati td.pos {{ font-family: {COND}; font-size: 32px; }}
table.dati td.pt {{ font-family: {COND}; font-size: 34px; }}
table.dati small {{ display: block; font-family: Georgia, serif; font-size: 24px; }}
/* Georgia ha numeri "all'antica" (lo 0 sembra una o): cifre in bastoni */
.num, table.dati td:not(.sq), .mini td:last-child, .mini td:first-child::first-line, .prob, .firma, .lato, .dataline, .sommario b,
.folio .info, .byline, .gara .meta, .cifre .k, .capo .k {{
  font-family: {BAST};
}}
table.dati tr.nostra td {{ background: {CIANO}; font-weight: 700; }}
.gara {{ border-bottom: 1px solid {NAVY}; padding: 10px 0 12px; }}
.gara .meta {{ display: flex; justify-content: space-between; align-items: center; font-size: 24px; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px; }}
.gara .meta .noi {{ background: {CIANO}; padding: 3px 10px; }}
.gara .riga {{ display: grid; grid-template-columns: 1fr 190px 1fr; align-items: center; gap: 20px; font-size: 32px; font-weight: 700; }}
.gara .riga .c {{ text-align: right; }}
.gara .ris {{ background: {NAVY}; color: #fff; font-family: {COND}; font-size: 52px; line-height: 1; text-align: center; padding: 2px 0; }}
.gara .ris.vs {{ background: #fff; color: {NAVY}; border: 3px solid {NAVY}; font-size: 36px; padding: 8px 0; text-transform: uppercase; }}
.gara .mar {{ font-size: 24px; line-height: 1.3; margin-top: 6px; font-style: italic; }}
.gara.nostra {{ border-left: 10px solid {CIANO}; padding-left: 20px; }}
.prob {{ display: flex; height: 38px; margin-top: 8px; border: 2px solid {NAVY}; font-size: 24px; }}
.prob div {{ display: flex; align-items: center; justify-content: center; overflow: hidden; white-space: nowrap; }}
.prob .p1 {{ background: {NAVY}; color: #fff; }} .prob .px {{ background: #fff; }} .prob .p2 {{ background: {CIANO}; }}
.legenda {{ font-size: 24px; margin-top: 14px; }}
.due {{ display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }}
.sezbar {{ background: {NAVY}; color: #fff; font-family: {BAST}; font-weight: 700; font-size: 24px; letter-spacing: 3px; text-transform: uppercase; padding: 8px 14px; }}
.capo {{ background: {CIANO}; padding: 12px 18px 16px; display: grid; grid-template-columns: auto 1fr; gap: 4px 18px; align-items: center; }}
.capo .k {{ grid-column: 1 / -1; font-size: 24px; letter-spacing: 1px; text-transform: uppercase; }}
.capo .v {{ font-family: {COND}; font-size: 110px; line-height: .9; }}
.capo .chi {{ font-size: 26px; font-weight: 700; line-height: 1.2; }}
.capo .chi small {{ display: block; font-weight: 400; font-size: 24px; }}
.due table.dati {{ font-size: 24px; }}
.due table.dati td {{ padding: 10px 6px; }}
/* Pagina di Zanni: i blocchi ciano diventano rosa (testatina, occhiello,
   gioco di parole, nome della firma); testata e firma restano quelle di sempre */
.zanni .folio .sez, .zanni .occhiello, .zanni .titolo .gioco, .zanni .byline .nome, .zanni .cit {{ background: {ROSA}; }}
.zanni .cit {{ background: none; border-top-color: {ROSA}; }}
.zanni .tab-int .mar {{ border-top-color: {ROSA}; }}
.richiami .occ.zanni {{ background: {ROSA}; }}
/* Loghi ufficiali delle squadre: piccoli, accanto al nome, mai al posto del nome */
.stemma {{ display: inline-block; vertical-align: middle; object-fit: contain; width: 1.25em; height: 1.25em; margin: 0 .35em; }}
table.dati td.sq .stemma, .mini .stemma {{ margin-left: 0; }}
.punteggio .stemma {{ width: 56px; height: 56px; margin: 0; background: #fff; border-radius: 50%; padding: 4px; }}
.tab-int .stemma {{ width: 54px; height: 54px; background: #fff; border-radius: 50%; padding: 4px; }}
.firma {{ position: absolute; left: 40px; right: 56px; bottom: {ZONA_BASSO}px; height: 80px; border-top: 3px solid {NAVY}; display: flex; align-items: center; gap: 16px; font-size: 24px; }}
.firma svg {{ width: 50px; height: 50px; flex: none; }}
"""

CONTROLLO = """<script>
window.addEventListener('load', function () {
  // Il titolone parte grande e si stringe finché sta in larghezza, in al massimo
  // due righe e senza spingere fuori pagina il resto della prima pagina.
  var c = document.querySelector('.contenuto');
  var t = document.querySelector('.titolone');
  var pieno = function () { return c.scrollHeight > c.clientHeight + 1; };
  // Pagine interne: una riga sola se ci sta ad almeno 88px, altrimenti due righe
  // da 120px in giù. Non si stringe per far posto al testo: un pezzo troppo
  // lungo va tagliato.
  var h = document.querySelector('.titolo');
  if (h) {
    var z = 120;
    h.style.whiteSpace = 'nowrap';
    while (z > 88 && h.scrollWidth > h.clientWidth) { z -= 4; h.style.fontSize = z + 'px'; }
    if (h.scrollWidth > h.clientWidth) {
      h.style.whiteSpace = 'normal';
      z = 120;
      h.style.fontSize = z + 'px';
      var righe = function () { return Math.round(h.getBoundingClientRect().height / z); };
      while (z > 64 && (righe() > 2 || h.scrollWidth > h.clientWidth)) { z -= 4; h.style.fontSize = z + 'px'; }
    }
  }
  // Come in edicola: se il titolo sta su una riga a corpo pieno, la riempie;
  // altrimenti va su due righe.
  if (t) {
    var s = 300;
    t.style.whiteSpace = 'nowrap';
    t.style.fontSize = s + 'px';
    while (s > 150 && (t.scrollWidth > t.clientWidth || pieno())) { s -= 4; t.style.fontSize = s + 'px'; }
    if (t.scrollWidth > t.clientWidth || pieno()) {
      t.style.whiteSpace = 'normal';
      s = 230;
      var troppo = function () {
        var righe = Math.round(t.getBoundingClientRect().height / s);
        return t.scrollWidth > t.clientWidth || righe > 2 || pieno();
      };
      t.style.fontSize = s + 'px';
      while (s > 80 && troppo()) { s -= 4; t.style.fontSize = s + 'px'; }
    }
  }
  var fuori = c && c.scrollHeight > c.clientHeight + 1;
  document.body.setAttribute('data-overflow', fuori ? 'si' : 'no');
});
</script>"""


def e(testo):
    return html.escape(str(testo))


def titolo_html(parti):
    """Un titolo è una stringa oppure una lista di parti: stringhe e ("testo", True) per il gioco di parole."""
    if isinstance(parti, str):
        return e(parti)
    out = []
    for p in parti:
        if isinstance(p, (tuple, list)):
            out.append(f'<span class="gioco">{e(p[0])}</span>' if p[1] else e(p[0]))
        else:
            out.append(e(p))
    return "".join(out)


def titolo_testo(parti):
    if isinstance(parti, str):
        return parti
    return "".join(p[0] if isinstance(p, (tuple, list)) else p for p in parti)


def svg_icona(dim):
    return (
        f'<svg viewBox="0 0 256 256" width="{dim}" height="{dim}">'
        f'<rect width="256" height="256" fill="{CIANO}"/>'
        '<clipPath id="ic"><rect width="256" height="256"/></clipPath>'
        f'<g clip-path="url(#ic)">{logo.drago(18, 36, 0.86, NAVY)}</g></svg>'
    )


def filigrana():
    return f'<svg class="filigrana" viewBox="0 0 256 256"><g fill="{NAVY}">{logo.DRAGO}</g></svg>'


def pagina(u, titolo_doc, corpo, top, testata_grande=False, classe=""):
    numero = f"N° {u['numero']}"
    if testata_grande:
        testa = (
            '<div class="testata"><svg viewBox="16 16 736 224">'
            f"{logo.testata(NAVY, CIANO, NAVY, numero)}</svg></div>"
            f'<div class="dataline"><span>{e(u["data_uscita"])}</span>'
            f'<span>{e(u["giornata"])}ª giornata · {e(u["girone"])}</span></div>'
        )
    else:
        testa = f'<div class="testata"><svg viewBox="0 0 768 96">{logo.compatta(NAVY, CIANO, NAVY, numero)}</svg></div>'
    return f"""<!doctype html>
<html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=1080">
<title>{e(titolo_doc)} · La Gazzetta del Dragone {e(numero)}</title>
<style>{CSS}</style></head>
<body><div class="pagina {classe}">
{filigrana()}
<div class="lato">{e(FIRMA)} · {e(numero)}</div>
{testa}
<div class="contenuto" style="--top:{top}px">
{corpo}
</div>
<div class="firma">{svg_icona(50)}<span>{e(FIRMA)} · {e(numero)}</span></div>
</div>
{CONTROLLO}
</body></html>
"""


def immagine(percorso, base):
    if not percorso:
        return '<span class="segnaposto">Immagine di copertina</span>'
    p = percorso if os.path.isabs(percorso) else os.path.join(base, percorso)
    mime = mimetypes.guess_type(p)[0] or "image/jpeg"
    with open(p, "rb") as fh:
        dati = base64.b64encode(fh.read()).decode()
    return f'<img src="data:{mime};base64,{dati}" alt="">'


LOGHI = os.path.join(RADICE, "logo")
_stemmi = {}


def stemma(nome):
    """Logo ufficiale della squadra da logo/, incorporato nella pagina. Un file
    vale per una squadra se tutte le parole del suo nome compaiono nel nome della
    squadra ("amici renato" per "Amici Di Renato"). Senza file, niente logo."""
    if nome not in _stemmi:
        parole = set(re.findall(r"\w+", nome.lower()))
        trovato = ""
        if os.path.isdir(LOGHI):
            for f in sorted(os.listdir(LOGHI)):
                radice, est = os.path.splitext(f)
                if est.lower() in (".png", ".jpg", ".jpeg", ".webp", ".svg") and set(re.findall(r"\w+", radice.lower())) <= parole:
                    trovato = immagine(os.path.join(LOGHI, f), LOGHI).replace("<img ", '<img class="stemma" ')
                    break
        _stemmi[nome] = trovato
    return _stemmi[nome]


def prob_html(prob, casa, ospite):
    if not prob:
        return ""
    p1, px, p2 = prob
    return (
        f'<div class="prob" title="{e(casa)} / pareggio / {e(ospite)}">'
        f'<div class="p1" style="width:{p1}%">1 · {p1}%</div>'
        f'<div class="px" style="width:{px}%">X · {px}%</div>'
        f'<div class="p2" style="width:{p2}%">2 · {p2}%</div></div>'
    )


RUBRICHE = [
    ("classifica", "Classifica", "La classifica completa dopo la giornata"),
    ("risultati", "Risultati", "Tutte le gare, con le probabilità della vigilia"),
    ("marcatori-assist", "Marcatori e assist", "Chi segna e chi serve: le classifiche"),
    ("prossimo-turno", "Prossimo turno", "Le partite che vengono, con le probabilità"),
    ("partita-settimana", "La partita della settimana", "La gara più attesa del prossimo turno"),
]


# Gare per pagina nelle rubriche risultati e prossimo turno: con 7 gare a
# giornata la rubrica va su due pagine, legate da "continua a" e "segue da".
GARE_PAGINA = 4


def a_blocchi(gare):
    if len(gare) <= GARE_PAGINA:
        return [gare]
    # la prima pagina ha anche titolo, numeri e rimando: una gara in meno
    prima = GARE_PAGINA - 1
    return [gare[:prima]] + [gare[i:i + GARE_PAGINA] for i in range(prima, len(gare), GARE_PAGINA)]


def pagine_rubriche(u):
    """(slug, nome, descrizione, prima pagina, quante pagine) per ogni rubrica."""
    quante = {
        "risultati": len(a_blocchi(u["risultati"])),
        "prossimo-turno": len(a_blocchi(u["prossimo_turno"])),
    }
    n, out = len(u["articoli"]) + 1, []
    for slug_, nome, desc in RUBRICHE:
        if slug_ == "partita-settimana" and not u.get("partita_settimana"):
            continue  # rubrica senza trafiletto: non esce
        k = quante.get(slug_, 1)
        out.append((slug_, nome, desc, n, k))
        n += k
    return out


def pag(n):
    return f'<span class="rimando">pag. {n:02d}</span>'


def copertina(u, base):
    """Prima pagina sul modello dei quotidiani sportivi: l'apertura è il primo
    articolo, la spalla porta il dato e la classifica, il taglio basso richiama
    gli altri pezzi e le rubriche con il numero di pagina."""
    c = u["copertina"]
    arts = u["articoli"]
    p_classifica = len(arts) + 1

    punteggio = ""
    if c.get("punteggio"):
        s = c["punteggio"]
        punteggio = (
            f'<div class="punteggio">{stemma(s["casa"])}<span>{e(s["casa"])}</span><b>{e(s["risultato"])}</b>'
            f'<span>{e(s["ospite"])}</span>{stemma(s["ospite"])}</div>'
        )
    didascalia = f'<figcaption>{e(c["didascalia"])}</figcaption>' if c.get("didascalia") else ""

    nostra = u.get("squadra_nostra")
    primi3 = "".join(
        f'<tr{" class=nostra" if r[1] == nostra else ""}><td>{r[0]}. {stemma(r[1])}{e(r[1])}</td><td><b>{r[2]}</b></td></tr>'
        for r in u["classifica"][:3]
    )
    dato = c["dato"]


    # le parti successive di un pezzo diviso non hanno un richiamo proprio
    richiami = [
        (a["occhiello"], titolo_testo(a["titolo"]), a["sommario"], i, a.get("firma", "Redazione"))
        for i, a in enumerate(arts[1:], 2)
        if a.get("parte", 1) == 1
    ]
    for _, nome, desc, prima, _ in pagine_rubriche(u):
        if len(richiami) >= 3:
            break
        if nome == "Classifica":
            continue  # già in prima pagina, nella spalla
        richiami.append(("Rubrica", nome, desc, prima, "Redazione"))
    taglio = "".join(
        f'<div><span class="occ titoli{" zanni" if f == "Gianluca Zanni" else ""}">{e(o)}</span><h4>{e(t)}</h4>'
        + (f'<span class="di">di {e(f)}</span>' if f != "Redazione" else "")
        + f"{pag(n)}</div>"
        for o, t, s, n, f in richiami[:3]
    )

    corpo = f"""
<div class="sopra"><span class="kicker titoli">{e(c["occhiello"])}</span><span class="testo-sopra">{e(c["sopratitolo"])}</span></div>
<h1 class="titolone">{titolo_html(c["titolo"])}</h1>
<p class="catenaccio">{e(c["catenaccio"])} {pag(1)}</p>
<div class="apertura">
  <figure class="foto">{immagine(c.get("immagine"), base)}{punteggio}{didascalia}</figure>
  <aside class="spalla">
    <div class="blocco"><h3>Il dato</h3><span class="grande">{e(dato["valore"])}</span>{e(dato["testo"])}</div>
    <div class="blocco"><h3>Classifica</h3><table class="mini">{primi3}</table>{pag(p_classifica)}</div>
  </aside>
</div>
<div class="richiami">{taglio}</div>"""
    return pagina(u, "Prima pagina", f'<div class="cop">{corpo}</div>', top=TOP_COP, testata_grande=True)


def folio(u, n, sezione):
    """Testatina delle pagine interne: numero di pagina, sezione, giornata."""
    return (
        f'<div class="folio"><span class="pg">{n:02d}</span><span class="sez titoli">{e(sezione)}</span>'
        f'<span class="info">{e(u["giornata"])}ª giornata · {e(u["data_uscita"])}</span></div>'
    )


def cifre(voci, alto=False):
    """Box dei numeri: (etichetta, valore, testo). Solo dati veri o calcolati dai dati."""
    if not voci:
        return ""
    celle = "".join(
        f'<div><span class="k">{e(k)}</span><span class="v">{e(v)}</span>{e(t)}</div>' for k, v, t in voci
    )
    return f'<div class="cifre{" alto" if alto else ""}" style="grid-template-columns:repeat({len(voci)},1fr)">{celle}</div>'


def testa_int(u, n, sezione, occhiello, titolo, catenaccio):
    # nelle rubriche il titolo dice già tutto: occhiello None, niente etichetta doppia
    occ = f'<div class="occhiello titoli">{e(occhiello)}</div>' if occhiello else ""
    return (
        f'{folio(u, n, sezione)}{occ}'
        f'<h1 class="titolo">{titolo_html(titolo)}</h1><p class="cat-int">{e(catenaccio)}</p>'
    )


def articolo(u, a, n, base, da=None, segue=None):
    """Pagina articolo. `da` e `segue` sono le pagine della parte precedente e
    successiva quando un pezzo lungo è diviso su più pagine."""
    paragrafi = [f"<p>{e(p)}</p>" for p in a["testo"]]
    c = a.get("citazione")
    if c:
        # dopo il secondo capoverso, mai in apertura
        cit = f'<blockquote class="cit">«{e(c["testo"])}»<cite>{e(c["autore"])}</cite></blockquote>'
        paragrafi.insert(max(1, min(2, len(paragrafi) - 1)), cit)
    testo = "".join(paragrafi)

    tab = ""
    m = a.get("partita")
    if m is not None:
        m = u["risultati"][m] if isinstance(m, int) else m
        mar = f'<div class="mar">Marcatori: {e(m["marcatori"])}</div>' if m.get("marcatori") else ""
        tab = (
            f'<div class="tab-int"><span class="c">{e(m["casa"])}{stemma(m["casa"])}</span><b>{e(m["risultato"])}</b>'
            f'<span>{stemma(m["ospite"])}{e(m["ospite"])}</span>{mar}</div>'
        )
    foto = ""
    if a.get("immagine"):
        cap = f'<figcaption>{e(a["didascalia"])}</figcaption>' if a.get("didascalia") else ""
        foto = f'<figure class="foto foto-int">{immagine(a["immagine"], base)}{cap}</figure>'

    chi = a.get("firma", "Redazione")
    if chi == "Redazione":
        byline = '<div class="byline"><span>di Redazione</span>'
    else:
        # pezzo firmato da un giornalista: il nome si vede come in un quotidiano
        prima = "La cronaca di" if a.get("tipo") == "cronaca" else "di"
        byline = f'<div class="byline autore"><span>{prima} <b class="nome">{e(chi)}</b></span>'
    if da:
        # pagina di seguito: niente titolone, solo il titolo in piccolo e il rimando,
        # così il testo ha quasi tutta la pagina
        testa = (
            f'{folio(u, n, a.get("sezione", "La giornata"))}'
            f'<div class="seguito"><span class="titolo-seguito">{e(titolo_testo(a["titolo"]))}</span>'
            f'<span class="segue">segue da {pag(da)}</span></div>'
        )
    else:
        testa = (
            f'{testa_int(u, n, a.get("sezione", "La giornata"), a["occhiello"], a["titolo"], a["sommario"])}\n'
            f'{byline}<span>{e(u["girone"])}</span></div>\n{foto}{tab}'
        )
    corpo = f"""<div class="int">
{testa}
<div class="colonne">{testo}</div>
{f'<div class="segue">continua a {pag(segue)}</div>' if segue else ""}
{cifre(a.get("numeri", []))}
</div>"""
    return pagina(u, titolo_testo(a["titolo"]), corpo, top=TOP_INT, classe="zanni" if a.get("tipo") == "cronaca" else "")


def gol(risultato):
    m = re.match(r"\s*(\d+)\s*-\s*(\d+)", str(risultato))
    return (int(m.group(1)), int(m.group(2))) if m else None


def rubrica_classifica(u, n):
    cl = u["classifica"]
    nostra = u.get("squadra_nostra")
    righe = []
    for r in cl:
        pos, sq, pt, g, v, nn, p, gf, gs = r
        c = ' class="nostra"' if sq == nostra else ""
        righe.append(
            f"<tr{c}><td class='pos'>{pos}</td><td class='sq'>{stemma(sq)}{e(sq)}</td><td class='pt'>{pt}</td><td>{g}</td>"
            f"<td>{v}</td><td>{nn}</td><td>{p}</td><td>{gf}</td><td>{gs}</td><td>{gf - gs:+d}</td></tr>"
        )
    # numeri calcolati dalla classifica, nessun dato aggiunto
    voci = [("Capolista", cl[0][2], cl[0][1])]
    noi = next((r for r in cl if r[1] == nostra), None)
    if noi:
        distacco = cl[0][2] - noi[2]
        voci.append(("Noi", f"{noi[0]}ª", f"{nostra}, " + ("in vetta" if noi[0] == 1 else f"a {distacco} punti dalla vetta")))
    att = max(cl, key=lambda r: r[7])
    dif = min(cl, key=lambda r: r[8])
    voci.append(("Attacco", att[7], att[1]))
    voci.append(("Difesa", dif[8], dif[1]))

    corpo = f"""<div class="int">
{testa_int(u, n, "Il girone", None, "La classifica", f"Dopo la {u['giornata']}ª giornata · {u['girone']}")}
{cifre(voci, alto=True)}
<table class="dati"><tr><th>#</th><th class="sq">Squadra</th><th>PT</th><th>G</th><th>V</th><th>N</th><th>P</th><th>GF</th><th>GS</th><th>DR</th></tr>
{"".join(righe)}</table>
</div>"""
    return pagina(u, "Classifica", corpo, top=TOP_INT)


def blocco_partita(u, m, giocata):
    nostra = u.get("squadra_nostra") in (m["casa"], m["ospite"])
    centro = (
        f'<div class="ris">{e(m["risultato"])}</div>' if giocata else '<div class="ris vs">vs</div>'
    )
    meta = f'<span>{e(m.get("data", ""))}</span>' + ('<span class="noi">La nostra gara</span>' if nostra else "")
    mar = f'<div class="mar">Marcatori: {e(m["marcatori"])}</div>' if giocata and m.get("marcatori") else ""
    return (
        f'<div class="gara{" nostra" if nostra else ""}"><div class="meta">{meta}</div>'
        f'<div class="riga"><div class="c">{e(m["casa"])}{stemma(m["casa"])}</div>{centro}<div>{stemma(m["ospite"])}{e(m["ospite"])}</div></div>'
        f'{mar}{prob_html(m.get("prob"), m["casa"], m["ospite"])}</div>'
    )


def testa_seguito(u, n, sezione, titolo, da):
    """Testata delle pagine di seguito: folio, titolo in piccolo e rimando."""
    return (
        f'{folio(u, n, sezione)}<div class="seguito"><span class="titolo-seguito">{e(titolo)}</span>'
        f'<span class="segue">segue da {pag(da)}</span></div>'
    )


def rubrica_gare(u, n, gare, giocate, sezione, titolo, catenaccio, cifre_html, nome):
    """Una o più pagine di gare (risultati o prossimo turno), GARE_PAGINA per pagina."""
    blocchi = a_blocchi(gare)
    pagine = []
    for k, blocco in enumerate(blocchi):
        p = n + k
        if k == 0:
            testa = f"{testa_int(u, p, sezione, None, titolo, catenaccio)}{cifre_html}"
        else:
            testa = testa_seguito(u, p, sezione, titolo, p - 1)
        segue = f'<div class="segue">continua a {pag(p + 1)}</div>' if k + 1 < len(blocchi) else ""
        corpo = f"""<div class="int">
{testa}
{"".join(blocco_partita(u, m, giocate) for m in blocco)}
{segue}
</div>"""
        pagine.append(pagina(u, nome, corpo, top=TOP_INT))
    return pagine


def rubrica_risultati(u, n):
    punteggi = [gol(m["risultato"]) for m in u["risultati"]]
    punteggi = [p for p in punteggi if p]
    voci = []
    if punteggi:
        voci = [
            ("Gol", sum(a + b for a, b in punteggi), f"in {len(punteggi)} gare"),
            ("Segno 1", sum(a > b for a, b in punteggi), "in casa"),
            ("Segno X", sum(a == b for a, b in punteggi), "pareggi"),
            ("Segno 2", sum(a < b for a, b in punteggi), "fuori"),
        ]
    return rubrica_gare(
        u, n, u["risultati"], True, "La giornata", f"Risultati della {u['giornata']}ª",
        "Marcatori e probabilità della vigilia", cifre(voci, alto=True), "Risultati",
    )


def con_posizione(righe):
    """Posizioni a pari merito: chi ha lo stesso numero ha la stessa posizione."""
    out, pos, prima = [], 0, None
    for i, (nome, sq, v) in enumerate(righe, 1):
        if v != prima:
            pos, prima = i, v
        out.append((pos, nome, sq, v))
    return out


def colonna_classifica(titolo, etichetta, righe, col):
    r = con_posizione(righe)
    if not r:
        return f'<div><div class="sezbar">{e(titolo)}</div></div>'
    primi = [x for x in r if x[0] == 1]
    # nel box vanno al massimo tre nomi; con più primi a pari merito restano in tabella
    nel_box = len(primi) <= 3
    if nel_box:
        chi = "".join(f"<div>{e(x[1])}<small>{e(x[2])}</small></div>" for x in primi)
    else:
        chi = f"<div>{len(primi)} giocatori<small>a pari merito</small></div>"
    capo = (
        f'<div class="capo"><span class="k">{e(etichetta)}</span>'
        f'<span class="v">{e(primi[0][3])}</span><div class="chi">{chi}</div></div>'
    )
    resto = "".join(
        f"<tr><td class='pos'>{p}</td><td class='sq'>{e(nome)}<small>{e(sq)}</small></td><td class='pt'>{v}</td></tr>"
        for p, nome, sq, v in r
        if not (nel_box and p == 1)
    )
    tabella = (
        f"<table class='dati'><tr><th style='width:70px'>#</th><th class='sq'>Giocatore</th>"
        f"<th style='width:100px'>{e(col)}</th></tr>{resto}</table>"
        if resto
        else ""
    )
    return f'<div><div class="sezbar">{e(titolo)}</div>{capo}{tabella}</div>'


def rubrica_marcatori(u, n):
    nota = u.get("nota_marcatori", "")
    cat = f"Le classifiche stagionali dopo la {u['giornata']}ª giornata" + (f" · {nota}" if nota else "")
    corpo = f"""<div class="int">
{testa_int(u, n, "Statistiche", None, "Chi segna e chi serve", cat)}
<div class="due">
{colonna_classifica("Marcatori", "Capocannoniere", u["marcatori"], "Gol")}
{colonna_classifica("Assist", "Re degli assist", u["assist"], "Assist")}
</div>
</div>"""
    return pagina(u, "Marcatori e assist", corpo, top=TOP_INT)


def rubrica_prossimo(u, n):
    g = u["giornata"] + 1
    return rubrica_gare(
        u, n, u["prossimo_turno"], False, "Il prossimo turno", f"Verso la {g}ª giornata",
        "Le gare con le probabilità della vigilia", "", "Prossimo turno",
    )


def posizioni(u):
    return {r[1]: (r[0], r[2]) for r in u["classifica"]}


def scegli_partita(u):
    """La partita della settimana: la gara del prossimo turno più equilibrata.
    Con le probabilità vince la differenza più piccola tra vittoria in casa e
    in trasferta; a parità, o senza probabilità, la coppia più in alto in
    classifica (somma delle posizioni più bassa), poi quella più vicina in
    punti. Restituisce (indice in prossimo_turno, motivo)."""
    pos = posizioni(u)
    voti = []
    for i, m in enumerate(u["prossimo_turno"]):
        (pc, ptc), (po, pto) = pos[m["casa"]], pos[m["ospite"]]
        pr = m.get("prob")
        voti.append((abs(pr[0] - pr[2]) if pr else 0, pc + po, abs(ptc - pto), i))
    d, somma, gap, i = min(voti)
    m = u["prossimo_turno"][i]
    if all(x.get("prob") for x in u["prossimo_turno"]):
        motivo = f"probabilità più vicine (scarto {d} punti percentuali)"
    else:
        motivo = "senza probabilità: la coppia più in alto in classifica"
    return i, f"{m['casa']} - {m['ospite']}: {motivo}, somma delle posizioni {somma}, {gap} punti di distanza"


def rubrica_partita(u, n):
    """Trafiletto sulla partita della settimana. La gara si sceglie da sola
    (scegli_partita) salvo indice esplicito; il testo lo scrive la redazione."""
    ps = u["partita_settimana"]
    i = ps.get("indice", scegli_partita(u)[0])
    m = u["prossimo_turno"][i]
    pos = posizioni(u)
    (pc, ptc), (po, pto) = pos[m["casa"]], pos[m["ospite"]]
    voci = [
        (m["casa"], f"{pc}ª", f"{ptc} punti"),
        (m["ospite"], f"{po}ª", f"{pto} punti"),
        ("Distanza", abs(ptc - pto), "punti in classifica"),
    ]
    if m.get("prob"):
        voci.append(("Pareggio", f"{m['prob'][1]}%", "alla vigilia"))
    testo = "".join(f"<p>{e(p)}</p>" for p in ps["testo"])
    corpo = f"""<div class="int">
{testa_int(u, n, "Il prossimo turno", "La partita della settimana", ps["titolo"], ps["sommario"])}
<div class="byline"><span>di Redazione</span><span>{e(u["girone"])}</span></div>
{blocco_partita(u, m, False)}
<div class="colonne" style="margin-top:22px">{testo}</div>
{cifre(voci)}
</div>"""
    return pagina(u, "La partita della settimana", corpo, top=TOP_INT)


def slug(testo):
    s = re.sub(r"[^a-z0-9]+", "-", testo.lower().encode("ascii", "ignore").decode())
    return s.strip("-")[:40] or "articolo"


def testi_md(u):
    righe = [f"# La Gazzetta del Dragone, N° {u['numero']} ({u['giornata']}ª giornata)\n"]
    c = u["copertina"]
    righe.append(f"## Copertina\n\n**Titolo:** {titolo_testo(c['titolo'])}\n\n**Catenaccio:** {c['catenaccio']}\n")
    for i, a in enumerate(u["articoli"], 1):
        righe.append(f"## {i:02d}. {titolo_testo(a['titolo'])}\n")
        chi = a.get("firma", "Redazione")
        if chi != "Redazione":
            righe.append(f"*Testo di {chi}: si pubblica come l'ha scritto, NON passarlo in Humanizer.*\n")
        righe.append(f"**Occhiello:** {a['occhiello']}\n\n**Sommario:** {a['sommario']}\n")
        righe.append("\n\n".join(a["testo"]) + "\n")
    ps = u.get("partita_settimana")
    if ps:
        righe.append(f"## La partita della settimana: {titolo_testo(ps['titolo'])}\n")
        righe.append(f"**Sommario:** {ps['sommario']}\n")
        righe.append("\n\n".join(ps["testo"]) + "\n")
    return "\n".join(righe)


def prepara(u):
    """Valori di base della cronaca firmata: sezione, occhiello e tabellino
    della nostra partita, se non sono indicati nel file dei contenuti."""
    nostra = u.get("squadra_nostra")
    for a in u["articoli"]:
        if a.get("tipo") != "cronaca":
            continue
        a.setdefault("sezione", "La nostra partita")
        a.setdefault("occhiello", "La cronaca")
        if "partita" not in a:
            for i, m in enumerate(u["risultati"]):
                if nostra in (m["casa"], m["ospite"]):
                    a["partita"] = i
                    break


def carica(percorso):
    spec = importlib.util.spec_from_file_location("contenuti_uscita", percorso)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.USCITA


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sorgente = os.path.abspath(sys.argv[1])
    u = carica(sorgente)
    prepara(u)
    cartella = u.get("cartella", f"giornata-{u['giornata']:02d}")
    out = os.path.join(RADICE, "uscite", cartella)
    os.makedirs(out, exist_ok=True)

    base = os.path.dirname(sorgente)
    pagine = [("00-copertina.html", copertina(u, base))]
    arts = u["articoli"]
    n = 1
    for i, a in enumerate(arts):
        # un pezzo diviso: le parti sono articoli consecutivi con "parte" 1, 2, ...
        da = n - 1 if a.get("parte", 1) > 1 else None
        dopo = arts[i + 1] if i + 1 < len(arts) else {}
        segue = n + 1 if a.get("parte") and dopo.get("parte") == a["parte"] + 1 else None
        nome = a.get("slug") or slug(titolo_testo(a["titolo"]))
        pagine.append((f"{n:02d}-{nome}.html", articolo(u, a, n, base, da, segue)))
        n += 1
    fn = {
        "classifica": rubrica_classifica,
        "risultati": rubrica_risultati,
        "marcatori-assist": rubrica_marcatori,
        "prossimo-turno": rubrica_prossimo,
        "partita-settimana": rubrica_partita,
    }
    if u.get("prossimo_turno") and u.get("classifica"):
        print("partita della settimana (scelta automatica):", scegli_partita(u)[1])
    for nome, _, _, prima, _ in pagine_rubriche(u):
        fatte = fn[nome](u, prima)
        fatte = fatte if isinstance(fatte, list) else [fatte]
        for k, html in enumerate(fatte):
            suff = f"-{k + 1}" if len(fatte) > 1 else ""
            pagine.append((f"{prima + k:02d}-{nome}{suff}.html", html))

    for nome, contenuto in pagine:
        with open(os.path.join(out, nome), "w", encoding="utf-8") as fh:
            fh.write(contenuto)
        print("scritta", nome)

    md = os.path.join(RADICE, "uscite", f"{cartella}-articoli.md")
    with open(md, "w", encoding="utf-8") as fh:
        fh.write(testi_md(u))
    print("scritto", os.path.basename(md))


if __name__ == "__main__":
    main()
