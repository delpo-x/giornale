# La Gazzetta del Dragone: guida al logo

## L'idea
Una testata da quotidiano classico, con doppi filetti, nome con le grazie e due orecchiette ai lati. A sinistra c'è la testa del drago di profilo, rivolta a sinistra come nel logo IMPLAST: è il richiamo alla squadra. A destra ci sono il numero dell'uscita e il girone.

## File
| File | Uso |
|---|---|
| `testata-colore.svg` | Copertina (`00-copertina.html`), in alto, su fondo bianco |
| `testata-negativo.svg` | Su fondo blu navy |
| `testata-navy.svg` | Versione a un colore (stampa, timbri, fondi chiari non bianchi) |
| `testata-compatta.svg` | Testata ridotta per le pagine degli articoli e delle rubriche |
| `testata-compatta-negativo.svg` | Testata ridotta su fondo navy |
| `icona.svg` | Simbolo piccolo: firma a piè di pagina, avatar, filigrana |
| `drago.svg` | Solo la testa del drago, navy, per usi grafici liberi |
| `prova-copertina.svg`, `prova-articolo.svg` | Prove di impaginazione 1080x1920 (non da pubblicare) |
| `png/` | Anteprime raster |

Per rigenerare tutto (per esempio con un altro numero di uscita): `python genera_logo.py <cartella>`.

## Colori
| Nome | HEX | Uso |
|---|---|---|
| Blu navy | `#0A2342` | Testi, filetti, drago |
| Azzurro ciano | `#00A8E8` | Solo blocchi: riquadro del drago, pannelli, evidenziazioni |
| Bianco | `#FFFFFF` | Sfondo |

Il ciano non si usa mai come testo sottile su bianco, perché ha poco contrasto. Si usa come blocco, con testo o drago navy sopra.

## Regole
- Il numero nell'orecchietta destra va aggiornato a ogni uscita.
- Spazio libero intorno alla testata: almeno l'altezza della riga "La Gazzetta del".
- Larghezza minima: testata grande 600 px, testata compatta 400 px. Sotto queste misure si usa `icona.svg`.
- Non deformare, ruotare o ricolorare la testata, e non aggiungere ombre o sfumature.
- Il drago resta sempre rivolto a sinistra.
- La firma in fondo a ogni pagina usa l'icona più la dicitura "© Redazione La Gazzetta del Dragone, tutti i diritti riservati · N° X".

## Da chiudere
- **Font:** le scritte usano Georgia come segnaposto. Vanno allineate ai font già incorporati in `template/genera_uscita.py`. Per un SVG del tutto autonomo, le scritte vanno convertite in tracciati con un font a licenza libera.
- **Marchio:** nessuna verifica legale è stata fatta.
