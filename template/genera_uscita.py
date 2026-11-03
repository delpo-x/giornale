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
FIRMA = "© Redazione La Gazzetta del Dragone, tutti i diritti riservati"

CSS = f"""
@page {{ size: 1080px 1920px; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 1080px; height: 1920px; background: #fff; }}
body {{
  color: {NAVY};
  font-family: Georgia, 'Times New Roman', serif;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}}
.pagina {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; padding: 40px 56px 0 40px; }}
.filigrana {{ position: absolute; right: -120px; bottom: 120px; width: 760px; opacity: .045; pointer-events: none; }}
.lato {{
  position: absolute; right: 10px; top: 50%; transform: translateY(-50%) rotate(90deg);
  transform-origin: center; white-space: nowrap; font-size: 15px; letter-spacing: 3px;
  text-transform: uppercase; opacity: .7; width: 0; display: flex; justify-content: center;
}}
.testata svg {{ display: block; width: 1000px; height: auto; }}
.dataline {{
  display: flex; justify-content: space-between; font-size: 22px; letter-spacing: 2px;
  text-transform: uppercase; padding: 10px 0 0;
}}
.contenuto {{ position: absolute; left: 40px; right: 56px; top: var(--top); bottom: 150px; overflow: hidden; }}
.titoli {{ font-family: 'Franklin Gothic Demi', 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif; }}
.gioco {{ background: {CIANO}; color: {NAVY}; padding: 0 14px; -webkit-box-decoration-break: clone; box-decoration-break: clone; }}
.foto {{ width: 1000px; height: 500px; background: {CIANO}; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
.foto img {{ width: 100%; height: 100%; object-fit: cover; }}
.foto span {{ font-size: 26px; letter-spacing: 3px; text-transform: uppercase; }}
.titolone {{ font-size: 92px; line-height: 1.02; margin: 34px 0 20px; text-transform: uppercase; }}
.catenaccio {{ font-size: 32px; line-height: 1.35; font-style: italic; margin-bottom: 28px; }}
.sommario {{ list-style: none; border-top: 4px solid {NAVY}; }}
.sommario li {{ display: flex; gap: 20px; align-items: baseline; padding: 14px 0; border-bottom: 1px solid {NAVY}; font-size: 28px; line-height: 1.25; }}
.sommario b {{ font-family: 'Franklin Gothic Demi', Arial, sans-serif; font-size: 30px; min-width: 48px; }}
.riquadri {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-top: 28px; }}
.riquadro {{ border: 5px solid {CIANO}; padding: 18px; font-size: 23px; line-height: 1.3; }}
.riquadro h3 {{ background: {CIANO}; margin: -18px -18px 14px; padding: 8px 18px; font-size: 22px; letter-spacing: 2px; text-transform: uppercase; }}
.riquadro .grande {{ font-size: 54px; line-height: 1; display: block; margin: 6px 0; }}
.mini td {{ padding: 3px 0; }} .mini td:last-child {{ text-align: right; font-weight: 700; }}
.mini {{ width: 100%; border-collapse: collapse; }}
.occhiello {{ display: inline-block; background: {CIANO}; padding: 8px 18px; font-size: 24px; letter-spacing: 3px; text-transform: uppercase; margin: 36px 0 22px; }}
.titolo {{ font-size: 76px; line-height: 1.04; margin-bottom: 22px; }}
.sommario-art {{ font-size: 33px; line-height: 1.35; font-style: italic; padding-bottom: 26px; margin-bottom: 30px; border-bottom: 4px solid {NAVY}; }}
.testo p {{ font-size: 30px; line-height: 1.5; margin-bottom: 18px; text-align: left; hyphens: auto; }}
.testo p:first-child::first-letter {{ font-family: 'Franklin Gothic Demi', Arial, sans-serif; float: left; font-size: 104px; line-height: .86; padding: 6px 12px 0 0; }}
.parte {{ font-size: 22px; letter-spacing: 3px; text-transform: uppercase; margin-top: 10px; }}
table.dati {{ width: 100%; border-collapse: collapse; font-size: 28px; }}
table.dati th {{ font-family: 'Franklin Gothic Demi', Arial, sans-serif; font-weight: 400; text-align: center; padding: 10px 6px; border-bottom: 4px solid {NAVY}; font-size: 24px; letter-spacing: 1px; }}
table.dati td {{ text-align: center; padding: 13px 6px; border-bottom: 1px solid {NAVY}; }}
table.dati td.sq, table.dati th.sq {{ text-align: left; }}
/* Georgia ha numeri "all'antica" (lo 0 sembra una o): cifre in bastoni */
.num, table.dati td:not(.sq), .mini td:last-child, .mini td:first-child::first-line, .prob, .firma, .lato, .dataline, .sommario b {{
  font-family: 'Franklin Gothic Demi', 'Franklin Gothic Medium', Arial, sans-serif;
}}
table.dati tr.nostra td {{ background: {CIANO}; font-weight: 700; }}
.partita {{ border-bottom: 1px solid {NAVY}; padding: 20px 0; }}
.partita .riga {{ display: grid; grid-template-columns: 1fr 170px 1fr; align-items: center; font-size: 34px; }}
.partita .riga .c {{ text-align: right; }}
.partita .ris {{ font-family: 'Franklin Gothic Demi', Arial, sans-serif; font-size: 50px; text-align: center; }}
.partita .ris.vs {{ font-size: 30px; }}
.partita .note {{ font-size: 22px; line-height: 1.35; margin-top: 8px; }}
.partita.nostra {{ background: linear-gradient({CIANO}, {CIANO}) left / 10px 100% no-repeat; padding-left: 22px; }}
.prob {{ display: flex; height: 34px; margin-top: 12px; border: 2px solid {NAVY}; font-size: 19px; }}
.prob div {{ display: flex; align-items: center; justify-content: center; overflow: hidden; white-space: nowrap; }}
.prob .p1 {{ background: {NAVY}; color: #fff; }} .prob .px {{ background: #fff; }} .prob .p2 {{ background: {CIANO}; }}
.legenda {{ font-size: 20px; margin-top: 18px; }}
.sezione {{ font-size: 30px; letter-spacing: 2px; text-transform: uppercase; margin: 6px 0 12px; }}
.firma {{ position: absolute; left: 40px; right: 56px; bottom: 40px; height: 80px; border-top: 3px solid {NAVY}; display: flex; align-items: center; gap: 16px; font-size: 22px; }}
.firma svg {{ width: 50px; height: 50px; flex: none; }}
"""

CONTROLLO = """<script>
window.addEventListener('load', function () {
  var c = document.querySelector('.contenuto');
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
        f'<g clip-path="url(#ic)">{logo.drago(10, 47, 0.9, NAVY)}</g></svg>'
    )


def filigrana():
    return f'<svg class="filigrana" viewBox="0 0 256 256"><g fill="{NAVY}">{logo.DRAGO}</g></svg>'


def pagina(u, titolo_doc, corpo, top, testata_grande=False):
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
<body><div class="pagina">
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
        return '<div class="foto"><span>Immagine di copertina</span></div>'
    p = percorso if os.path.isabs(percorso) else os.path.join(base, percorso)
    mime = mimetypes.guess_type(p)[0] or "image/jpeg"
    with open(p, "rb") as fh:
        dati = base64.b64encode(fh.read()).decode()
    return f'<div class="foto"><img src="data:{mime};base64,{dati}" alt=""></div>'


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


def copertina(u, base):
    c = u["copertina"]
    voci = "".join(
        f"<li><b>{i:02d}</b><span>{e(titolo_testo(a['titolo']))}</span></li>"
        for i, a in enumerate(u["articoli"], 1)
    )
    top5 = "".join(
        f'<tr><td>{r[0]}. {e(r[1])}</td><td>{r[2]}</td></tr>' for r in u["classifica"][:5]
    )
    simbolo = c["partita_simbolo"]
    dato = c["dato"]
    corpo = f"""
{immagine(c.get("immagine"), base)}
<h1 class="titolone titoli">{titolo_html(c["titolo"])}</h1>
<p class="catenaccio">{e(c["catenaccio"])}</p>
<ol class="sommario">{voci}</ol>
<div class="riquadri">
  <div class="riquadro"><h3>Classifica</h3><table class="mini">{top5}</table></div>
  <div class="riquadro"><h3>Partita simbolo</h3>{e(simbolo["partita"])}<span class="grande titoli">{e(simbolo["risultato"])}</span>{e(simbolo["nota"])}</div>
  <div class="riquadro"><h3>Il dato</h3><span class="grande titoli">{e(dato["valore"])}</span>{e(dato["testo"])}</div>
</div>"""
    return pagina(u, "Prima pagina", corpo, top=410, testata_grande=True)


def articolo(u, a):
    paragrafi = "".join(f"<p>{e(p)}</p>" for p in a["testo"])
    parte = f'<div class="parte">Parte {a["parte"]}</div>' if a.get("parte") else ""
    corpo = f"""
<div class="occhiello titoli">{e(a["occhiello"])}</div>
<h1 class="titolo titoli">{titolo_html(a["titolo"])}</h1>
<p class="sommario-art">{e(a["sommario"])}</p>
<div class="testo">{paragrafi}</div>{parte}"""
    return pagina(u, titolo_testo(a["titolo"]), corpo, top=170)


def rubrica_classifica(u):
    righe = []
    for r in u["classifica"]:
        pos, sq, pt, g, v, n, p, gf, gs = r
        cl = ' class="nostra"' if sq == u.get("squadra_nostra") else ""
        righe.append(
            f"<tr{cl}><td>{pos}</td><td class='sq'>{e(sq)}</td><td><b>{pt}</b></td><td>{g}</td>"
            f"<td>{v}</td><td>{n}</td><td>{p}</td><td>{gf}</td><td>{gs}</td><td>{gf - gs:+d}</td></tr>"
        )
    corpo = f"""
<div class="occhiello titoli">Rubrica</div>
<h1 class="titolo titoli">Classifica</h1>
<p class="sommario-art">Dopo la {e(u["giornata"])}ª giornata · {e(u["girone"])}</p>
<table class="dati"><tr><th>#</th><th class="sq">Squadra</th><th>PT</th><th>G</th><th>V</th><th>N</th><th>P</th><th>GF</th><th>GS</th><th>DR</th></tr>
{"".join(righe)}</table>"""
    return pagina(u, "Classifica", corpo, top=170)


def blocco_partita(u, m, giocata):
    nostra = u.get("squadra_nostra") in (m["casa"], m["ospite"])
    centro = (
        f'<div class="ris">{e(m["risultato"])}</div>' if giocata else '<div class="ris vs">vs</div>'
    )
    note = []
    if m.get("data"):
        note.append(e(m["data"]))
    if giocata and m.get("marcatori"):
        note.append("Marcatori: " + e(m["marcatori"]))
    return (
        f'<div class="partita{" nostra" if nostra else ""}">'
        f'<div class="riga"><div class="c">{e(m["casa"])}</div>{centro}<div>{e(m["ospite"])}</div></div>'
        f'<div class="note">{" · ".join(note)}</div>'
        f'{prob_html(m.get("prob"), m["casa"], m["ospite"])}</div>'
    )


def rubrica_risultati(u):
    corpo = f"""
<div class="occhiello titoli">Rubrica</div>
<h1 class="titolo titoli">Risultati</h1>
<p class="sommario-art">{e(u["giornata"])}ª giornata · probabilità pre-partita sotto ogni gara</p>
{"".join(blocco_partita(u, m, True) for m in u["risultati"])}
<p class="legenda">1 vittoria casa · X pareggio · 2 vittoria ospite</p>"""
    return pagina(u, "Risultati", corpo, top=170)


def rubrica_marcatori(u):
    def tab(righe, col):
        r = "".join(
            f"<tr><td>{i}</td><td class='sq'>{e(n)} <small>· {e(s)}</small></td><td><b>{v}</b></td></tr>"
            for i, (n, s, v) in enumerate(righe, 1)
        )
        return (
            "<table class='dati'><tr><th style='width:60px'>#</th><th class='sq'>Giocatore</th>"
            f"<th style='width:130px'>{col}</th></tr>{r}</table>"
        )

    nota = u.get("nota_marcatori", "")
    corpo = f"""
<div class="occhiello titoli">Rubrica</div>
<h1 class="titolo titoli">Marcatori e assist</h1>
<p class="sommario-art">Classifiche stagionali dopo la {e(u["giornata"])}ª giornata{(" · " + e(nota)) if nota else ""}</p>
<div class="sezione titoli">Marcatori</div>{tab(u["marcatori"], "Gol")}
<div class="sezione titoli" style="margin-top:34px">Assist</div>{tab(u["assist"], "Assist")}"""
    return pagina(u, "Marcatori e assist", corpo, top=170)


def rubrica_prossimo(u):
    corpo = f"""
<div class="occhiello titoli">Rubrica</div>
<h1 class="titolo titoli">Prossimo turno</h1>
<p class="sommario-art">{e(u["giornata"] + 1)}ª giornata · probabilità pre-partita</p>
{"".join(blocco_partita(u, m, False) for m in u["prossimo_turno"])}
<p class="legenda">1 vittoria casa · X pareggio · 2 vittoria ospite</p>"""
    return pagina(u, "Prossimo turno", corpo, top=170)


def slug(testo):
    s = re.sub(r"[^a-z0-9]+", "-", testo.lower().encode("ascii", "ignore").decode())
    return s.strip("-")[:40] or "articolo"


def testi_md(u):
    righe = [f"# La Gazzetta del Dragone, N° {u['numero']} ({u['giornata']}ª giornata)\n"]
    c = u["copertina"]
    righe.append(f"## Copertina\n\n**Titolo:** {titolo_testo(c['titolo'])}\n\n**Catenaccio:** {c['catenaccio']}\n")
    for i, a in enumerate(u["articoli"], 1):
        righe.append(f"## {i:02d}. {titolo_testo(a['titolo'])}\n")
        righe.append(f"**Occhiello:** {a['occhiello']}\n\n**Sommario:** {a['sommario']}\n")
        righe.append("\n\n".join(a["testo"]) + "\n")
    return "\n".join(righe)


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
    cartella = u.get("cartella", f"giornata-{u['giornata']:02d}")
    out = os.path.join(RADICE, "uscite", cartella)
    os.makedirs(out, exist_ok=True)

    pagine = [("00-copertina.html", copertina(u, os.path.dirname(sorgente)))]
    n = 1
    for a in u["articoli"]:
        pagine.append((f"{n:02d}-{a.get('slug') or slug(titolo_testo(a['titolo']))}.html", articolo(u, a)))
        n += 1
    for nome, fn in (
        ("classifica", rubrica_classifica),
        ("risultati", rubrica_risultati),
        ("marcatori-assist", rubrica_marcatori),
        ("prossimo-turno", rubrica_prossimo),
    ):
        pagine.append((f"{n:02d}-{nome}.html", fn(u)))
        n += 1

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
