"""Ricava il tracciato vettoriale della testa del drago dall'immagine sorgente.

Uso: python assets/logo/traccia_drago.py [immagine] [precisione]

Sorgente di base: assets/logo/sorgente/drago.jpg (silhouette navy su bianco,
generata da Nicola). Il risultato va in assets/logo/drago-path.txt: un solo
tracciato in un riquadro 256x256, centrato in orizzontale e appoggiato al
bordo basso (il collo è tagliato lì). genera_logo.py lo legge da quel file.
Serve OpenCV (cv2).
"""
import os
import sys

import cv2

QUI = os.path.dirname(os.path.abspath(__file__))


def traccia(percorso, precisione=0.8):
    img = cv2.imread(percorso, cv2.IMREAD_GRAYSCALE)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    _, bw = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
    # RETR_CCOMP tiene anche i buchi (occhio, narice): si riempiono con evenodd
    contorni, _ = cv2.findContours(bw, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    contorni = [c for c in contorni if cv2.contourArea(c) > 400]  # via i puntini di rumore
    x0 = min(c[:, 0, 0].min() for c in contorni)
    x1 = max(c[:, 0, 0].max() for c in contorni)
    y0 = min(c[:, 0, 1].min() for c in contorni)
    y1 = max(c[:, 0, 1].max() for c in contorni)
    s = 256 / max(x1 - x0, y1 - y0)
    dx = (256 - (x1 - x0) * s) / 2
    dy = 256 - (y1 - y0) * s
    parti = []
    for c in contorni:
        punti = cv2.approxPolyDP(c, precisione, True)[:, 0]
        parti.append("M" + " L".join(f"{(x - x0) * s + dx:.1f} {(y - y0) * s + dy:.1f}" for x, y in punti) + "Z")
    return "".join(parti)


def main():
    sorgente = sys.argv[1] if len(sys.argv) > 1 else os.path.join(QUI, "sorgente", "drago.jpg")
    precisione = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8
    d = traccia(sorgente, precisione)
    with open(os.path.join(QUI, "drago-path.txt"), "w", encoding="utf-8") as fh:
        fh.write(d + "\n")
    print("scritto drago-path.txt,", len(d), "caratteri")


if __name__ == "__main__":
    main()
