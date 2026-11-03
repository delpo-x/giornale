"""Esporta ogni pagina HTML di un'uscita in PNG 1080x1920 e PDF.

Uso: python template/esporta.py uscite/giornata-07

I file finiscono in uscite/giornata-07/export/. Lo script segnala le pagine
in cui il testo esce dall'area utile: vanno accorciate o divise in due.
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

CANDIDATI = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "chromium",
]


def trova_browser():
    for c in CANDIDATI:
        if os.path.isfile(c) or shutil.which(c):
            return c
    sys.exit("Chrome o Edge non trovati: servono per l'esportazione.")


def chrome(browser, profilo, *argomenti):
    base = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        "--force-device-scale-factor=1",
        f"--user-data-dir={profilo}",
        "--window-size=1080,1920",
        "--virtual-time-budget=3000",
    ]
    return subprocess.run(base + list(argomenti), capture_output=True, text=True, encoding="utf-8", errors="ignore")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    cartella = os.path.abspath(sys.argv[1])
    pagine = sorted(glob.glob(os.path.join(cartella, "*.html")))
    if not pagine:
        sys.exit(f"Nessuna pagina HTML in {cartella}")
    out = os.path.join(cartella, "export")
    os.makedirs(out, exist_ok=True)
    browser = trova_browser()
    problemi = []

    with tempfile.TemporaryDirectory() as profilo:
        for p in pagine:
            nome = os.path.splitext(os.path.basename(p))[0]
            url = "file:///" + p.replace("\\", "/")
            png = os.path.join(out, nome + ".png")
            pdf = os.path.join(out, nome + ".pdf")
            chrome(browser, profilo, f"--screenshot={png}", url)
            chrome(browser, profilo, f"--print-to-pdf={pdf}", "--no-pdf-header-footer", url)
            dom = chrome(browser, profilo, "--dump-dom", url).stdout
            m = re.search(r'data-overflow="(si|no)"', dom)
            stato = m.group(1) if m else "?"
            ok = os.path.isfile(png) and os.path.isfile(pdf)
            if stato == "si":
                problemi.append(f"{nome}: il testo esce dalla pagina")
            elif stato == "?":
                problemi.append(f"{nome}: controllo del testo non riuscito")
            if not ok:
                problemi.append(f"{nome}: PNG o PDF mancante")
            print(f"{'OK ' if ok and stato == 'no' else '!! '} {nome}")

    if problemi:
        print("\nDa sistemare:")
        for r in problemi:
            print(" -", r)
        sys.exit(1)
    print(f"\nTutto esportato in {out}")


if __name__ == "__main__":
    main()
