"""Genera le varianti SVG della testata "La Gazzetta del Dragone".

Uso: python genera_logo.py <cartella-di-uscita>
"""
import os
import sys

NAVY = "#0A2342"
CIANO = "#00A8E8"
BIANCO = "#FFFFFF"

SERIF = "Georgia, 'Times New Roman', serif"
# Georgia ha numeri "all'antica" (lo 0 sembra una o): i numeri vanno in bastoni.
BASTONI = "'Franklin Gothic Demi', 'Franklin Gothic Medium', Arial, sans-serif"

# Testa del drago in un riquadro 256x256, rivolta a sinistra come nel logo IMPLAST:
# centrata in orizzontale, collo tagliato sul bordo basso. Il tracciato viene da
# sorgente/drago.jpg tramite traccia_drago.py.
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "drago-path.txt"), encoding="utf-8") as _fh:
    DRAGO = f'<path fill-rule="evenodd" d="{_fh.read().strip()}"/>'


def drago(x, y, scala, colore):
    return f'<g transform="translate({x} {y}) scale({scala})" fill="{colore}">{DRAGO}</g>'


def svg(vb, corpo, titolo, sfondo=None):
    w, h = vb
    bg = f'<rect width="{w}" height="{h}" fill="{sfondo}"/>' if sfondo else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
        f"<title>{titolo}</title>{bg}{corpo}</svg>\n"
    )


def testata(inchiostro, blocco, drago_col, numero="N° 7"):
    """Testata completa 768x256: filetti, orecchiette, nome."""
    c = []
    for y, h in ((20, 6), (32, 2), (222, 2), (230, 6)):
        c.append(f'<rect x="16" y="{y}" width="736" height="{h}" fill="{inchiostro}"/>')
    # orecchietta sinistra: blocco con il drago (richiamo IMPLAST)
    c.append(f'<rect x="24" y="56" width="112" height="144" fill="{blocco}"/>')
    # il collo esce dal fondo del riquadro: lo taglio con un clip
    c.append('<clipPath id="ear"><rect x="24" y="56" width="112" height="144"/></clipPath>')
    c.append(f'<g clip-path="url(#ear)">{drago(20, 80, 0.47, drago_col)}</g>')
    # orecchietta destra: numero dell'uscita
    c.append(
        f'<path fill="{inchiostro}" fill-rule="evenodd" '
        'd="M632 56 H744 V200 H632 Z M638 62 H738 V194 H638 Z"/>'
    )
    c.append(
        f'<text x="688" y="114" font-family="{BASTONI}" font-size="26" '
        f'text-anchor="middle" fill="{inchiostro}">{numero}</text>'
    )
    c.append(f'<rect x="656" y="128" width="64" height="2" fill="{inchiostro}"/>')
    for y, t in ((154, "GIRONE"), (176, "CSI")):
        c.append(
            f'<text x="688" y="{y}" font-family="{SERIF}" font-size="15" letter-spacing="1" '
            f'text-anchor="middle" fill="{inchiostro}">{t}</text>'
        )
    c.append(
        f'<text x="384" y="92" font-family="{SERIF}" font-size="30" font-style="italic" '
        f'text-anchor="middle" fill="{inchiostro}">La Gazzetta del</text>'
    )
    c.append(
        f'<text x="384" y="176" font-family="{SERIF}" font-size="72" font-weight="700" '
        f'letter-spacing="1" text-anchor="middle" fill="{inchiostro}">DRAGONE</text>'
    )
    c.append(
        f'<text x="384" y="206" font-family="{SERIF}" font-size="13" letter-spacing="4" '
        f'text-anchor="middle" fill="{inchiostro}">IL QUOTIDIANO DEL GIRONE</text>'
    )
    return "".join(c)


def compatta(inchiostro, blocco, drago_col, numero="N° 7"):
    """Testata ridotta 768x96 per le pagine degli articoli."""
    c = [
        f'<rect x="0" y="4" width="768" height="4" fill="{inchiostro}"/>',
        f'<rect x="0" y="88" width="768" height="4" fill="{inchiostro}"/>',
        f'<rect x="0" y="16" width="64" height="64" fill="{blocco}"/>',
        '<clipPath id="earc"><rect x="0" y="16" width="64" height="64"/></clipPath>',
        f'<g clip-path="url(#earc)">{drago(3.8, 23.7, 0.22, drago_col)}</g>',
        f'<text x="384" y="64" text-anchor="middle" fill="{inchiostro}">'
        f'<tspan font-family="{SERIF}" font-size="24" font-style="italic">La Gazzetta del </tspan>'
        f'<tspan font-family="{SERIF}" font-size="40" font-weight="700" letter-spacing="1">DRAGONE</tspan></text>',
        f'<rect x="704" y="16" width="64" height="64" fill="{inchiostro}"/>',
        f'<text x="736" y="38" font-family="{BASTONI}" font-size="13" letter-spacing="1" '
        f'text-anchor="middle" fill="#FFFFFF">{numero.split()[0]}</text>',
        f'<text x="736" y="70" font-family="{BASTONI}" font-size="30" font-weight="700" '
        f'text-anchor="middle" fill="#FFFFFF">{numero.split()[-1]}</text>',
    ]
    return "".join(c)


FIRMA = "© Redazione La Gazzetta del Dragone, tutti i diritti riservati"


def firma(y, numero):
    return (
        f'<rect x="40" y="{y}" width="1000" height="3" fill="{NAVY}"/>'
        f'<rect x="40" y="{y + 16}" width="44" height="44" fill="{CIANO}"/>'
        '<clipPath id="fir"><rect x="40" y="' + str(y + 16) + '" width="44" height="44"/></clipPath>'
        f'<g clip-path="url(#fir)">{drago(42.8, y + 21.6, 0.15, NAVY)}</g>'
        f'<text x="100" y="{y + 46}" font-family="{SERIF}" font-size="22" fill="{NAVY}">'
        f"{FIRMA} · {numero}</text>"
    )


def prova_copertina(numero):
    """Prova 1080x1920 della prima pagina con la testata grande."""
    s = 1000 / 736
    c = [
        f'<g transform="translate({40 - 16 * s} 40) scale({s})">{testata(NAVY, CIANO, NAVY, numero)}</g>',
        f'<rect x="40" y="420" width="1000" height="500" fill="{CIANO}"/>',
        f'<rect x="40" y="970" width="860" height="70" fill="{NAVY}"/>',
        f'<rect x="40" y="1060" width="620" height="70" fill="{NAVY}"/>',
    ]
    for i in range(6):
        c.append(f'<rect x="40" y="{1180 + i * 40}" width="{1000 if i < 5 else 640}" height="14" fill="{NAVY}" opacity="0.35"/>')
    c.append(f'<rect x="40" y="1460" width="485" height="300" fill="none" stroke="{CIANO}" stroke-width="6"/>')
    c.append(f'<rect x="555" y="1460" width="485" height="300" fill="none" stroke="{CIANO}" stroke-width="6"/>')
    c.append(firma(1790, numero))
    return "".join(c)


def prova_articolo(numero):
    """Prova 1080x1920 di una pagina articolo con la testata ridotta."""
    s = 1000 / 768
    c = [
        f'<g transform="translate(40 40) scale({s})">{compatta(NAVY, CIANO, NAVY, numero)}</g>',
        f'<rect x="40" y="220" width="260" height="40" fill="{CIANO}"/>',
        f'<rect x="40" y="290" width="980" height="64" fill="{NAVY}"/>',
        f'<rect x="40" y="370" width="760" height="64" fill="{NAVY}"/>',
        f'<rect x="40" y="470" width="1000" height="22" fill="{NAVY}" opacity="0.6"/>',
        f'<rect x="40" y="506" width="700" height="22" fill="{NAVY}" opacity="0.6"/>',
    ]
    for i in range(24):
        w = 1000 if i % 8 != 7 else 560
        c.append(f'<rect x="40" y="{580 + i * 46}" width="{w}" height="14" fill="{NAVY}" opacity="0.35"/>')
    c.append(firma(1790, numero))
    return "".join(c)


def icona(blocco, drago_col):
    """Icona quadrata 256x256: blocco ciano con il drago."""
    return (
        f'<rect width="256" height="256" fill="{blocco}"/>'
        '<clipPath id="ico"><rect width="256" height="256"/></clipPath>'
        f'<g clip-path="url(#ico)">{drago(18, 36, 0.86, drago_col)}</g>'
    )


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    t = "La Gazzetta del Dragone"
    files = {
        "testata-colore.svg": svg((768, 256), testata(NAVY, CIANO, NAVY), t),
        "testata-navy.svg": svg((768, 256), testata(NAVY, NAVY, BIANCO), t),
        "testata-negativo.svg": svg((768, 256), testata(BIANCO, CIANO, NAVY), t, sfondo=NAVY),
        "testata-compatta.svg": svg((768, 96), compatta(NAVY, CIANO, NAVY), t),
        "testata-compatta-negativo.svg": svg((768, 96), compatta(BIANCO, CIANO, NAVY), t, sfondo=NAVY),
        "icona.svg": svg((256, 256), icona(CIANO, NAVY), t),
        "drago.svg": svg((256, 256), f'<g fill="{NAVY}">{DRAGO}</g>', t),
        "prova-copertina.svg": svg((1080, 1920), prova_copertina("N° 7"), t, sfondo=BIANCO),
        "prova-articolo.svg": svg((1080, 1920), prova_articolo("N° 7"), t, sfondo=BIANCO),
    }
    for name, content in files.items():
        with open(os.path.join(out, name), "w", encoding="utf-8") as fh:
            fh.write(content)
        print("scritto", name)


if __name__ == "__main__":
    main()
