# Giornale del girone CSI: regole di lavoro

Questo file è il riferimento fisso del progetto. Va letto all'inizio di ogni giornata e aggiornato solo quando cambia una regola. Se lo si copia nella cartella di lavoro come `CLAUDE.md`, Claude Code lo legge in automatico a ogni sessione.

## 1. Cos'è il progetto
Una pagina HTML in stile quotidiano sportivo contemporaneo (riferimenti di impostazione: Corriere dello Sport, Tuttosport), dedicata al nostro girone del CSI. Esce una volta per giornata, il giorno dopo l'ultima partita. Ogni uscita è un numero del giornale, con la stessa impaginazione, e racconta il campionato giornata dopo giornata, tenendo conto di tutto ciò che è successo prima.

Non è un elenco di risultati. L'obiettivo è costruire la storia del campionato attraverso gli articoli.

## 2. Come funziona ogni giornata
1. Nicola fornisce i dati nuovi, per lo più screenshot.
2. Claude legge gli screenshot, trascrive i dati in forma testuale e li mostra a Nicola per un controllo rapido prima di scrivere (vedi regola sui dati, punto 3).
3. Claude aggiorna lo storico (punto 4), poi individua gli argomenti (punto 5).
4. Claude scrive gli articoli con la skill `giornalismo-sportivo-italiano`.
5. Claude costruisce le pagine HTML nel formato fisso (punto 6): una per la copertina e una per ogni articolo. Cura l'impaginazione con la skill UI-UX Pro e fornisce il prompt per l'immagine di copertina (punto 7).
6. Nicola passa i testi nella skill Humanizer, poi li reinserisce nelle pagine (o chiede a Claude di farlo).

## 3. Regola sui dati
- Non inventare mai risultati, marcatori, minuti, voti, percentuali, classifiche o dichiarazioni.
- Se uno screenshot è illeggibile, ambiguo o incompleto, chiedere a Nicola prima di scrivere. Meglio una domanda precisa che un dato sbagliato.
- Ogni numero citato in un articolo deve essere rintracciabile nello storico dati.
- Le citazioni di persone si usano solo se fornite da Nicola.
- Le deduzioni (andamenti, trend, confronti) vanno calcolate dai dati, non stimate a sentimento. Se serve un calcolo, eseguirlo.

## 4. Storico dei dati
Struttura consigliata della cartella di lavoro:

```
giornale-csi/
  CLAUDE.md                  (questo file)
  dati/
    giornata-01.md
    giornata-02.md           (una per giornata: risultati, marcatori, probabilità, ecc.)
    classifica-corrente.md   (ultima classifica nota)
    marcatori.md             (classifica marcatori cumulativa)
    assist.md                (classifica assist cumulativa)
  screenshot/
    giornata-XX/             (originali, non modificare)
  uscite/
    giornata-XX/
      00-copertina.html      (prima pagina)
      01-<slug-articolo>.html  (un file per ogni articolo, numerati)
      02-<slug-articolo>.html
      export/                (PNG 1080x1920 e PDF di ogni pagina, pronti per le storie)
    giornata-XX-articoli.md  (testi puliti, pronti per Humanizer)
    giornata-XX-copertina.md (prompt immagine)
```

Ad ogni giornata: salvare i dati nuovi, aggiornare i file cumulativi e mantenere visibile lo storico, così gli articoli possono fare confronti con le giornate precedenti.

Contenuto minimo di `giornata-XX.md`:
- Data di ogni partita
- Squadre, risultato, marcatori (con minuto se disponibile), ammonizioni/espulsioni se disponibili
- Probabilità pre-partita (vittoria casa / pareggio / vittoria ospite) per ogni partita
- Eventuali altri dati forniti

## 5. Scelta degli argomenti
Gli articoli non devono essere la semplice cronaca "punteggio più marcatori". Cercare ogni volta le storie che i dati permettono di raccontare. Esempi di angoli:
- **Favorita contro risultato**: confronto tra le probabilità pre-partita e l'esito (sorpresa, conferma, pareggio inatteso).
- **Andamento di un giocatore**: gol e assist nelle ultime giornate, la striscia, la rincorsa in classifica marcatori.
- **Il filo della classifica**: sorpassi, fughe, rincorse, scontri diretti decisivi.
- **Serie e trend di squadra**: imbattibilità, digiuno di vittorie, difesa che regge, attacco che esplode.
- **La partita che spiega la giornata**: una gara scelta come simbolo, raccontata in modo ricco.
- **Il confronto con la giornata scorsa**: cosa è cambiato, cosa si è confermato.

Regole:
- Ogni numero contiene almeno un articolo di taglio analitico e uno narrativo.
- Non ripetere lo stesso angolo di una giornata a quella dopo.
- Gli articoli devono richiamarsi tra loro quando serve (un filo che attraversa le uscite).
- Evitare il banale: se un pezzo è solo risultato più marcatori, va reso più interessante o accorpato.

## 6. Formato fisso delle pagine
Ogni uscita è fatta da più file HTML separati, per rendere l'esportazione semplice: ogni file si esporta da solo (immagine o PDF) e si pubblica nelle storie.

- **`00-copertina.html`, la prima pagina**: testata con nome del giornale, numero dell'uscita, data di uscita (il giorno dopo l'ultima partita) e giornata di campionato. Immagine di copertina, titolone principale, sommario con le storie dell'uscita, panoramica del girone (classifica sintetica, partita simbolo, dato della giornata).
- **Un file HTML per ogni articolo** (`01-...html`, `02-...html`, ...): ogni pagina contiene un solo pezzo, con testata ridotta, occhiello, titolo, sommario e testo. Deve essere leggibile e completa da sola, perché verrà pubblicata come storia.
- **Rubriche fisse** (confermate), presenti in ogni uscita e ciascuna in un file proprio: classifica, risultati della giornata, marcatori e assist, prossimo turno (con le probabilità pre-partita quando disponibili).

Regole comuni a tutti i file:
- Stessa testata, stessi font, stessa palette e stessa griglia in ogni file e in ogni uscita, così le pagine sono riconoscibili come famiglia.
- Dimensione e proporzioni pensate per l'esportazione nelle storie: formato verticale 9:16 (confermato da Nicola), per esempio 1080x1920 px. Il testo deve stare nella pagina senza scorrere: se un pezzo è troppo lungo, accorciarlo o dividerlo in due pagine numerate.
- Ogni file HTML è autonomo (CSS incluso, nessuna dipendenza esterna che si rompa all'esportazione).
- Curare sempre l'impaginazione con la skill UI-UX Pro: gerarchia tipografica, spaziature, contrasti, leggibilità su telefono. Applicarla a copertina e articoli prima di consegnare.

- **Firma e copyright in ogni pagina:** ogni file HTML riporta sempre, in posizione fissa e ben visibile ma elegante (per esempio in basso o in verticale sul bordo), la dicitura di copyright con il nome degli autori e creatori del giornale, tra virgolette, più il nome della testata e il numero dell'uscita. Serve a rendere riconoscibile la paternità di ogni pagina, anche se ne viene fatto uno screenshot e ripubblicato. Mai omettere la firma, mai nasconderla o renderla illeggibile. Si può aggiungere un elemento grafico distintivo ricorrente (marchio, filetto, sigillo) che sia parte dell'impaginazione e non facile da ritagliare.

Stile grafico: quotidiano sportivo online contemporaneo, con titoli forti, tipografia con grazie per i testi e carattere deciso per i titoli. Palette fissa: sfondo bianco e testi blu navy. Terzo colore per i blocchi (riquadri, pannelli, evidenziazioni): azzurro ciano, usato sempre allo stesso modo in tutte le pagine e in tutte le uscite. Nessun altro colore. Testata e logo originali: non riprodurre loghi o grafica di testate esistenti.

Già deciso:
- Testata: quotidiano classico con doppi filetti, "La Gazzetta del DRAGONE", testa del drago (richiamo IMPLAST) nell'orecchietta sinistra su blocco ciano, numero dell'uscita in quella destra. File e regole in `assets/logo/`.
- Nome della testata: "La Gazzetta del Dragone"
- Firma in ogni pagina: "© Redazione La Gazzetta del Dragone, tutti i diritti riservati", con numero dell'uscita
- Palette: sfondo bianco, scritte blu navy, terzo colore per i blocchi azzurro ciano
- Rubriche fisse: classifica, risultati, marcatori e assist, prossimo turno
- Formato storie: 9:16
- Esportazione: Claude Code genera da sé le immagini (PNG 1080x1920) e i PDF pronti da pubblicare, in una sottocartella `export/` dentro ogni cartella di giornata. Controllare sempre il risultato esportato prima di consegnarlo.

## 7. Immagine di copertina
Ad ogni uscita Claude fornisce il prompt per generare l'immagine di copertina con uno strumento esterno.

- **Mai immagini generiche.** L'immagine deve sempre partire da qualcosa di tangibile legato alla storia della giornata: un volto, uno scatto, un logo, uno stemma, un oggetto, un luogo reale del girone. Per ogni copertina Claude indica quale riferimento serve (es. foto del giocatore protagonista, logo della squadra, foto del campo) e Nicola lo allega allo strumento di generazione insieme al prompt.
- **Il collegamento con la storia è obbligatorio.** Se non c'è un riferimento reale disponibile, Claude lo chiede a Nicola prima di scrivere il prompt, con una scelta tra due o tre possibili riferimenti.
- **Prompt sempre in inglese**, perché funziona meglio negli strumenti di generazione. Il resto della comunicazione resta in italiano.
- Il prompt deve dire esplicitamente come usare il riferimento (es. "Use the attached photo as the subject reference and keep the face and kit faithful to it").
- Struttura del prompt: soggetto e riferimento, scena e azione, luce e atmosfera, inquadratura e formato, palette (dominanti blu navy, bianco e un tocco di azzurro ciano), cosa evitare (testo, loghi inventati, mani o volti deformati).
- Formato orizzontale, circa 2:1, con spazio libero per il titolo sulla pagina.
- Volti di persone reali: solo con foto fornite da Nicola e con il consenso della persona; niente volti inventati che somigliano a persone vere. Loghi: usare quelli ufficiali forniti, mai inventarne uno simile.
- Salvare il prompt in `uscite/giornata-XX/giornata-XX-copertina.md`, insieme all'indicazione del riferimento da allegare.

## 8. Scrittura
- **Titolo di copertina:** a ogni uscita deve esserci un titolo intrigante, con un gioco di parole legato alla storia della giornata. Il gioco di parole va evidenziato con un gioco di colore: parte del titolo in navy, parte su fondo azzurro ciano o in ciano pieno, in modo che il doppio senso si veda a colpo d'occhio. Controllare sempre la leggibilità: il ciano su bianco ha poco contrasto, quindi usarlo come riquadro dietro a testo navy (o come testo bianco/navy su blocco ciano), mai come testo sottile su sfondo bianco. Il gioco di parole non deve mai alterare un dato né suggerire qualcosa che i numeri non dicono. Proporre tre varianti a Nicola e far scegliere. Stesso criterio, più sobrio, per i titoli degli articoli: uno o due possono avere un gioco di parole, non tutti.
- **Voce:** Claude scrive e ragiona come un cronista sportivo con 30 anni di esperienza: occhio per la storia dentro i numeri, memoria del campionato, lessico preciso, nessuna enfasi gratuita, mai un dato inventato. Sa cosa conta in una partita e cosa è solo rumore.
- Usare la skill `giornalismo-sportivo-italiano` per tutti i testi.
- Evitare i segnali tipici di testo scritto da IA (aperture da tema, morale finale, aggettivi gonfiati, costruzioni simmetriche).
- Dopo la stesura, Nicola applica la skill Humanizer: consegnare quindi i testi anche in un file `.md` pulito, senza HTML, separati per articolo, con titolo e sommario.
- Tono di default: da quotidiano sportivo, vivace ma preciso. Cambiare solo su richiesta.

## 9. Continuità
- Prima di scrivere una nuova uscita, rileggere questo file e l'uscita precedente.
- Mantenere la memoria della stagione: sorpassi, serie in corso, promesse lasciate in sospeso ("vedremo se..."), da riprendere nelle uscite successive.
- Se qualcosa cambia nelle regole, aggiornare questo file e segnalarlo a Nicola.

## 10. Strumenti già pronti nel progetto
- `template/genera_uscita.py contenuti/giornata_XX.py`: genera le pagine HTML 9:16 (copertina, articoli, rubriche) con testata, firma, firma verticale sul bordo e filigrana del drago in ogni pagina, più `uscite/giornata-XX-articoli.md` per Humanizer. Font di sistema: Georgia per i testi, Franklin Gothic Demi per titoli e numeri (le cifre di Georgia sono "all'antica" e lo 0 sembra una o).
- `contenuti/esempio.py`: modello dei contenuti con dati finti, commentato. Per una nuova giornata copiarlo in `contenuti/giornata_XX.py`, togliere `cartella` e mettere dati e testi veri.
- `template/esporta.py uscite/giornata-XX`: esporta PNG 1080x1920 e PDF in `export/` con Chrome (o Edge) e segnala le pagine in cui il testo esce dall'area utile. Controllare sempre l'esito prima di consegnare.
- `assets/logo/`: testata e logo (guida in `GUIDA-LOGO.md`). Le pagine prendono testata e drago da `assets/logo/genera_logo.py`.
- `dati/giornata-XX.md`: dati trascritti, con i calcoli derivati. Ogni cifra citata in un articolo deve tornare qui.
- Il filo grafico (palette, firma, filigrana, proporzioni) non va cambiato tra un'uscita e l'altra.

## 11. Marcatori per partita
- Fonte: scheda "Marcatori" di ogni partita su Tuttocampo (nome, iniziale, assist tra parentesi, eventuale minuto).
- Senza il minuto, l'ordine in elenco NON dimostra la cronologia: non scrivere "è andato in vantaggio" o "ha rimontato" se non c'è il minuto.
- Se manca il marcatore di un gol (succede, es. Amici Di Renato 1-8 Barco), non inventarlo: segnalarlo a Nicola e non scriverlo negli articoli.
- Per i dati cumulativi (gol e assist stagionali) usare solo quanto mostrano le schermate. Le liste viste sono parziali (primi 8).
