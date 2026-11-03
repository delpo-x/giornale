"""Contenuti di PROVA per controllare l'impaginazione. Tutti i dati sono finti.

Per una giornata vera: copiare questo file in contenuti/giornata_XX.py,
togliere "cartella", e sostituire tutto con i dati di dati/giornata-XX.md.

Titoli: una stringa, oppure una lista di parti dove ("testo", True)
finisce sul blocco ciano (il gioco di parole).
Probabilità: (casa, pareggio, ospite) in percentuale, somma 100.
Classifica: (pos, squadra, punti, giocate, vinte, pari, perse, gol fatti, gol subiti).
"""

PROVA = (
    "Testo di prova per misurare quanto spazio occupa un articolo vero nella pagina. "
    "Ogni riga serve solo a riempire la colonna e a vedere dove cade la fine del pezzo, "
    "senza alcun dato reale del girone."
)

USCITA = {
    "cartella": "esempio",
    "numero": 0,
    "giornata": 7,
    "girone": "Girone di prova",
    "data_uscita": "Data di prova",
    "squadra_nostra": "Squadra A",
    # Prima pagina. L'apertura è il primo articolo (pag. 01); il taglio basso
    # richiama gli altri articoli e le rubriche in automatico.
    "copertina": {
        "occhiello": "7ª giornata",
        "sopratitolo": "Sopratitolo di prova: il fatto in una riga, con il dato che lo spiega",
        "titolo": ["Titolo ", ("prova", True)],
        "catenaccio": "Catenaccio di prova: una o due righe che spiegano la storia principale.",
        "immagine": None,
        "didascalia": "Didascalia di prova: chi c'è nella foto e in quale momento.",
        "punteggio": {"casa": "Squadra A", "risultato": "0-0", "ospite": "Squadra B"},
        "dato": {"valore": "00", "testo": "Il dato della giornata, di prova."},
    },
    "articoli": [
        {
            "occhiello": "Analisi",
            "titolo": ["Primo articolo ", ("di prova", True)],
            "sommario": "Sommario di prova dell'articolo analitico, su due righe circa.",
            "testo": [PROVA, PROVA + " " + PROVA, PROVA, PROVA],
            # Facoltativi. "partita" è l'indice in "risultati" (o un dizionario):
            # mette il tabellino sotto la firma. "numeri": (etichetta, valore, testo).
            # "citazione" solo con parole dette davvero, mai inventate.
            "sezione": "La giornata",
            "citazione": {"testo": "Citazione di prova, da sostituire con parole vere.", "autore": "Nome di prova"},
            "numeri": [("Tiri", "00", "Dato di prova"), ("Possesso", "00%", "Dato di prova"), ("Falli", "00", "Dato di prova")],
        },
        {
            # La cronaca della nostra partita, scritta da Gianluca Zanni: il testo
            # è suo e si impagina com'è. Con "tipo": "cronaca" sezione, occhiello
            # e tabellino della nostra gara si mettono da soli.
            "tipo": "cronaca",
            "firma": "Gianluca Zanni",
            "titolo": "Cronaca di prova",
            "sommario": "Sommario di prova della cronaca firmata.",
            "testo": [PROVA, PROVA, PROVA],
            # Un pezzo lungo si divide in articoli consecutivi con "parte": 1, 2, ...
            # (le pagine si richiamano da sole con "continua a" e "segue da").
        },
    ],
    "classifica": [
        (1, "Squadra A", 0, 0, 0, 0, 0, 0, 0),
        (2, "Squadra B", 0, 0, 0, 0, 0, 0, 0),
        (3, "Squadra C", 0, 0, 0, 0, 0, 0, 0),
        (4, "Squadra D", 0, 0, 0, 0, 0, 0, 0),
        (5, "Squadra E", 0, 0, 0, 0, 0, 0, 0),
        (6, "Squadra F", 0, 0, 0, 0, 0, 0, 0),
        (7, "Squadra G", 0, 0, 0, 0, 0, 0, 0),
        (8, "Squadra H", 0, 0, 0, 0, 0, 0, 0),
    ],
    "risultati": [
        {"casa": "Squadra A", "ospite": "Squadra B", "risultato": "0-0", "data": "Data di prova", "marcatori": "Giocatore di prova", "prob": (40, 30, 30)},
        {"casa": "Squadra C", "ospite": "Squadra D", "risultato": "0-0", "data": "Data di prova", "marcatori": "Giocatore di prova (2), Giocatore di prova, Giocatore di prova", "prob": (50, 25, 25)},
        {"casa": "Squadra E", "ospite": "Squadra F", "risultato": "0-0", "data": "Data di prova", "marcatori": "Giocatore di prova (2), Giocatore di prova, Giocatore di prova", "prob": (20, 30, 50)},
        {"casa": "Squadra G", "ospite": "Squadra H", "risultato": "0-0", "data": "Data di prova", "marcatori": "Giocatore di prova (2), Giocatore di prova, Giocatore di prova", "prob": (34, 33, 33)},
    ],
    # Numeri finti, solo per vedere posizioni e pari merito.
    "marcatori": [(f"Giocatore {i}", "Squadra di prova", n) for i, n in enumerate((9, 7, 6, 6, 5, 4, 4, 3), 1)],
    "assist": [(f"Giocatore {i}", "Squadra di prova", n) for i, n in enumerate((6, 6, 5, 4, 3, 3, 2, 2), 1)],
    "nota_marcatori": "primi 8",
    "prossimo_turno": [
        {"casa": "Squadra B", "ospite": "Squadra C", "data": "Data di prova", "prob": (40, 30, 30)},
        {"casa": "Squadra D", "ospite": "Squadra A", "data": "Data di prova", "prob": (25, 25, 50)},
        {"casa": "Squadra F", "ospite": "Squadra G", "data": "Data di prova", "prob": (45, 30, 25)},
        {"casa": "Squadra H", "ospite": "Squadra E", "data": "Data di prova", "prob": (30, 30, 40)},
    ],
}
