"""Risultati del girone trascritti dagli screenshot di Tuttocampo
(screenshot/stagione-2026-11-03/). Una riga per gara: (data, casa, gol casa, gol ospite, ospite).
Gol None = gara non ancora giocata.

Uso: python dati/risultati.py  -> stampa la classifica calcolata e i controlli.
"""

GIRONE = "Amatori CSI · Calcio a 7 Serie C Open Brescia · Girone H"
NOSTRA = "Implast"

GIORNATE = {
    1: [
        ("ven 25 settembre", "Gso Monte", 2, 1, "Ieci Passirano"),
        ("ven 25 settembre", "F.c. Calino", 6, 3, "Nigoline"),
        ("ven 25 settembre", "Amici Di Renato", 2, 6, "Implast"),
        ("ven 25 settembre", "Bombetta", 4, 8, "Aston 5 Perle"),
        ("ven 25 settembre", "Gv Barco", 3, 3, "F.c. Cazzaghese"),
        ("sab 26 settembre", "Giaffa Clusan", 8, 2, "U.s. Pilzone"),
        ("sab 26 settembre", "Elettcristini", 6, 4, "Uso Borgonato"),
    ],
    2: [
        ("gio 1 ottobre", "Ieci Passirano", 1, 6, "Giaffa Clusan"),
        ("gio 1 ottobre", "U.s. Pilzone", 2, 4, "Amici Di Renato"),
        ("ven 2 ottobre", "Gv Barco", 3, 6, "Nigoline"),
        ("ven 2 ottobre", "Uso Borgonato", 7, 3, "Gso Monte"),
        ("sab 3 ottobre", "Aston 5 Perle", 0, 3, "Elettcristini"),
        ("sab 3 ottobre", "Implast", 2, 1, "F.c. Calino"),
        ("lun 5 ottobre", "F.c. Cazzaghese", 12, 2, "Bombetta"),
    ],
    3: [
        ("ven 9 ottobre", "Gso Monte", 5, 2, "Aston 5 Perle"),
        ("ven 9 ottobre", "F.c. Calino", 4, 1, "U.s. Pilzone"),
        ("ven 9 ottobre", "Uso Borgonato", 4, 1, "Ieci Passirano"),
        ("sab 10 ottobre", "Elettcristini", 4, 4, "F.c. Cazzaghese"),
        ("lun 12 ottobre", "Amici Di Renato", 2, 4, "Giaffa Clusan"),
        ("lun 12 ottobre", "Bombetta", 1, 5, "Nigoline"),
        ("mar 13 ottobre", "Gv Barco", 5, 0, "Implast"),
    ],
    4: [
        ("gio 15 ottobre", "Ieci Passirano", 0, 3, "Amici Di Renato"),
        ("gio 15 ottobre", "U.s. Pilzone", 4, 1, "Gv Barco"),
        ("ven 16 ottobre", "Nigoline", 4, 0, "Elettcristini"),
        ("sab 17 ottobre", "Aston 5 Perle", 2, 4, "Uso Borgonato"),
        ("sab 17 ottobre", "Giaffa Clusan", 0, 0, "F.c. Calino"),
        ("sab 17 ottobre", "Implast", 4, 3, "Bombetta"),
        ("lun 19 ottobre", "F.c. Cazzaghese", 7, 1, "Gso Monte"),
    ],
    5: [
        ("mer 21 ottobre", "F.c. Calino", 3, 7, "Amici Di Renato"),
        ("gio 22 ottobre", "Aston 5 Perle", 2, 4, "Ieci Passirano"),
        ("ven 23 ottobre", "Gso Monte", 3, 1, "Nigoline"),
        ("ven 23 ottobre", "Bombetta", 2, 7, "U.s. Pilzone"),
        ("ven 23 ottobre", "Gv Barco", 3, 3, "Giaffa Clusan"),
        ("sab 24 ottobre", "Elettcristini", 3, 5, "Implast"),
        ("mar 27 ottobre", "Uso Borgonato", 4, 9, "F.c. Cazzaghese"),
    ],
    6: [
        ("gio 29 ottobre", "Ieci Passirano", 2, 2, "F.c. Calino"),
        ("gio 29 ottobre", "U.s. Pilzone", 6, 3, "Elettcristini"),
        ("ven 30 ottobre", "F.c. Cazzaghese", 6, 2, "Aston 5 Perle"),
        ("ven 30 ottobre", "Amici Di Renato", 1, 8, "Gv Barco"),
        ("sab 31 ottobre", "Giaffa Clusan", 7, 0, "Bombetta"),
        ("sab 31 ottobre", "Implast", 5, 1, "Gso Monte"),
        ("mar 3 novembre, 20:30", "Nigoline", 4, 3, "Uso Borgonato"),
    ],
    7: [
        ("ven 6 novembre, 20:00", "Gso Monte", 3, 1, "U.s. Pilzone"),
        ("ven 6 novembre, 20:45", "F.c. Cazzaghese", 7, 0, "Ieci Passirano"),
        ("ven 6 novembre, 21:00", "Bombetta", 2, 6, "Amici Di Renato"),
        ("ven 6 novembre, 21:00", "Gv Barco", 1, 0, "F.c. Calino"),
        ("sab 7 novembre, 15:00", "Aston 5 Perle", 2, 4, "Nigoline"),
        ("sab 7 novembre, 17:30", "Elettcristini", 3, 4, "Giaffa Clusan"),
        ("mar 10 novembre, 21:00", "Uso Borgonato", 4, 4, "Implast"),
    ],
}

# Classifica ufficiale Tuttocampo dopo la 7ª (vista l'11 novembre): pt, v, n, p, dr.
UFFICIALE_G7 = {
    "F.c. Cazzaghese": (17, 5, 2, 0, 32), "Giaffa Clusan": (17, 5, 2, 0, 21),
    "Implast": (16, 5, 1, 1, 7), "Nigoline": (15, 5, 0, 2, 9),
    "Amici Di Renato": (12, 4, 0, 3, 0), "Gso Monte": (12, 4, 0, 3, -6),
    "Gv Barco": (11, 3, 2, 2, 7), "Uso Borgonato": (10, 3, 1, 3, 1),
    "U.s. Pilzone": (9, 3, 0, 4, -2), "F.c. Calino": (8, 2, 2, 3, 0),
    "Elettcristini": (7, 2, 1, 4, -5), "Ieci Passirano": (4, 1, 1, 5, -17),
    "Aston 5 Perle": (3, 1, 0, 6, -12), "Bombetta": (0, 0, 0, 7, -35),
}

# Statistiche squadra viste su Tuttocampo (prime 3), per il controllo incrociato.
# Viste prima di Nigoline 4-3 Borgonato: Borgonato gf e Nigoline gs ora differiscono di 3.
VISTE = {
    "gf": {"F.c. Cazzaghese": 41, "Giaffa Clusan": 28, "Uso Borgonato": 23},
    "gs": {"Giaffa Clusan": 8, "Nigoline": 13, "Implast": 15},
}


def classifica(fino_a=None):
    t = {}
    for g, gare in GIORNATE.items():
        if fino_a and g > fino_a:
            continue
        for _, c, gc, go, o in gare:
            for s in (c, o):
                t.setdefault(s, [0] * 7)  # pt g v n p gf gs
            if gc is None:
                continue
            for s, f, a in ((c, gc, go), (o, go, gc)):
                r = t[s]
                r[1] += 1
                r[5] += f
                r[6] += a
                if f > a:
                    r[0] += 3
                    r[2] += 1
                elif f == a:
                    r[0] += 1
                    r[3] += 1
                else:
                    r[4] += 1
    # ordine provvisorio: punti, differenza reti, gol fatti (i criteri CSI veri vanno verificati)
    return sorted(t.items(), key=lambda x: (-x[1][0], -(x[1][5] - x[1][6]), -x[1][5], x[0]))


if __name__ == "__main__":
    cl = classifica()
    print(f"{'#':>2} {'Squadra':18} PT  G  V  N  P  GF GS  DR")
    for i, (s, r) in enumerate(cl, 1):
        pt, g, v, n, p, gf, gs = r
        print(f"{i:>2} {s:18} {pt:>2} {g:>2} {v:>2} {n:>2} {p:>2} {gf:>3} {gs:>2} {gf - gs:+4d}")
    d = dict(cl)
    d6 = dict(classifica(6))  # VISTE risale alla 6ª giornata
    for k, idx in (("gf", 5), ("gs", 6)):
        for s, val in VISTE[k].items():
            stato = "ok" if d6[s][idx] == val else f"DIVERSO (calcolato {d6[s][idx]})"
            print(f"controllo {k} {s}: {val} {stato}")
    for s, (pt, v, n, p, dr) in UFFICIALE_G7.items():
        r = d[s]
        mio = (r[0], r[2], r[3], r[4], r[5] - r[6])
        if mio != (pt, v, n, p, dr):
            print(f"G7 DIVERSO {s}: ufficiale {(pt, v, n, p, dr)} calcolato {mio}")
    print("controllo classifica G7 finito")
