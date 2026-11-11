# Giornale del girone CSI: regole di lavoro

Questo file è il riferimento fisso del progetto. Va letto all'inizio di ogni giornata e aggiornato solo quando cambia una regola. Se lo si copia nella cartella di lavoro come `CLAUDE.md`, Claude Code lo legge in automatico a ogni sessione.

## 1. Cos'è il progetto
Una pagina HTML in stile quotidiano sportivo contemporaneo (riferimenti di impostazione: Corriere dello Sport, Tuttosport), dedicata al nostro girone del CSI. Esce una volta per giornata, il giorno dopo l'ultima partita. Ogni uscita è un numero del giornale, con la stessa impaginazione, e racconta il campionato giornata dopo giornata, tenendo conto di tutto ciò che è successo prima.

Non è un elenco di risultati. L'obiettivo è costruire la storia del campionato attraverso gli articoli.

## 2. Come funziona ogni giornata
1. Nicola fornisce i dati nuovi, per lo più screenshot. A ogni giornata Claude gli ricorda la lista di cosa serve, senza aspettare che se ne ricordi lui:
   - risultati e schede "Marcatori" di ogni gara;
   - classifica ufficiale;
   - classifica marcatori e classifica assist;
   - probabilità pre-partita;
   - Top 11;
   - calendario della giornata successiva;
   - pezzo di Zanni, se c'è;
   - **post Instagram delle squadre sulle proprie partite** (vedi sotto).
2. Claude legge gli screenshot, trascrive i dati in forma testuale e li mostra a Nicola per un controllo rapido prima di scrivere (vedi regola sui dati, punto 3).
3. Claude aggiorna lo storico (punto 4), poi individua gli argomenti (punto 5).
4. Claude scrive gli articoli con la skill `giornalismo-sportivo-italiano`. La cronaca della nostra partita la scrive Gianluca Zanni: Nicola la passa e Claude la impagina senza toccarla (punto 8).
5. Claude costruisce le pagine HTML nel formato fisso (punto 6): una per la copertina e una per ogni articolo. Cura l'impaginazione con la skill UI-UX Pro e fornisce il prompt per l'immagine di copertina (punto 7).
6. Claude passa ogni testo suo nella skill `humanizer` prima di consegnarlo (vedi punto 8, "Humanizer sempre"). Nelle pagine e nel file `.md` va solo la versione già passata.
7. **Revisione grafica prima della chiusura definitiva** (regola fissata da Nicola l'11 novembre, sempre): prima di consegnare l'uscita e di fare il commit, Claude passa le pagine esportate in queste skill:
   - `impeccable`: critica e rifinitura dell'impaginazione su copertina, articoli e rubriche (gerarchia, spazi, contrasti, leggibilità su telefono);
   - `emil-design-eng`: dettagli fini, cioè allineamenti, ritmo verticale, coerenza di filetti e etichette;
   - `break-ui`: prova del generatore con i casi peggiori (nomi di squadra lunghi, titoli lunghi, cinque marcatori in una gara, pari punti in classifica), per evitare sorprese come il 4-4 che andava a capo;
   - `apple-design`, solo per la tipografia: interlinea e spaziatura tra le lettere dei titoli.
   Il filo grafico resta fisso (punto 6): le modifiche al generatore che cambiano l'aspetto delle pagine si propongono a Nicola e si applicano solo con il suo sì. Le correzioni di difetti (testo che esce, righe che vanno a capo male) si fanno subito.

## 3. Regola sui dati
- Non inventare mai risultati, marcatori, minuti, voti, percentuali, classifiche o dichiarazioni.
- Se uno screenshot è illeggibile, ambiguo o incompleto, chiedere a Nicola prima di scrivere. Meglio una domanda precisa che un dato sbagliato.
- Ogni numero citato in un articolo deve essere rintracciabile nello storico dati.
- Le citazioni di persone si usano solo se fornite da Nicola.
- Le deduzioni (andamenti, trend, confronti) vanno calcolate dai dati, non stimate a sentimento. Se serve un calcolo, eseguirlo.

### Post Instagram delle squadre
Nicola può mandare gli screenshot dei post che le squadre pubblicano sui propri profili per commentare le loro partite. Sono contesto prezioso: il tono di una società, una dedica, un infortunio annunciato, l'umore dopo una sconfitta.
- Gli screenshot si salvano in `screenshot/giornata-XX/instagram/`. Il testo va trascritto in `dati/giornata-XX.md`, nella sezione "Dai profili delle squadre", con squadra, data e parole esatte.
- Negli articoli si può citare un post, tra virgolette e alla lettera, attribuendolo alla società ("scrive l'Implast sul suo profilo"). Non va attribuito a una persona, a meno che il post non sia firmato da quella persona.
- Un post è il punto di vista di una squadra, non un dato. Numeri e fatti presenti nel post (risultato, marcatori, minuti) vanno controllati con lo storico. Se non tornano, vale lo storico e la discrepanza si segnala a Nicola.
- Un fatto che compare solo in un post (per esempio un infortunio o un esordio) si scrive come "fa sapere la società", mai come certezza della redazione.
- Niente prese in giro o polemiche costruite sui post degli avversari: si possono raccontare, non deridere.

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
    giornata-XX-articoli.md  (testi puliti, già passati in humanizer)
    giornata-XX-copertina.md (prompt immagine)
```

File già in uso:
- `dati/stagione.md`: tutti i risultati, la classifica calcolata, le Top 11 e i controlli incrociati.
- `dati/risultati.py`: i risultati in forma calcolabile. `python dati/risultati.py` stampa la classifica e confronta i numeri con le statistiche di Tuttocampo.
- `dati/squadre.md`: l'anagrafica fissa delle squadre (staff, persone, note e curiosità). Ogni dato statico che Nicola manda va registrato qui, con la data, e si usa per arricchire gli articoli.

Il primo numero della Gazzetta esce il 4 novembre e racconta la 6ª giornata. Le giornate dalla 1 alla 5 sono contesto: entrano nei totali, nelle serie e nei confronti visti da oggi, ma non si raccontano e non hanno un'uscita propria (vedi "Solo attualità", punto 5). Da qui in avanti, numero N = giornata N + 5.

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
- **Solo attualità (regola fissata da Nicola il 3 novembre).** Ogni articolo parla della giornata appena giocata e della situazione di oggi. Le partite vecchie non si raccontano: niente pezzi, capoversi o richiami costruiti su gare delle giornate precedenti. Statistiche, serie, medie e confronti si fanno, ma partono sempre dall'oggi (classifica attuale, totali aggiornati, la gara appena giocata). Un dato del passato entra solo come numero che spiega il presente ("terza vittoria di fila", "12 gol in sei gare"), mai come racconto di quella partita. Lo stesso vale per la partita della settimana: si guarda avanti, non ai precedenti.
- Ogni numero contiene almeno un articolo di taglio analitico e uno narrativo.
- Non ripetere lo stesso angolo di una giornata a quella dopo.
- Gli articoli devono richiamarsi tra loro quando serve (un filo che attraversa le uscite).
- Evitare il banale: se un pezzo è solo risultato più marcatori, va reso più interessante o accorpato.

## 6. Formato fisso delle pagine
Ogni uscita è fatta da più file HTML separati, per rendere l'esportazione semplice: ogni file si esporta da solo (immagine o PDF) e si pubblica nelle storie.

- **`00-copertina.html`, la prima pagina**, costruita come quella di un quotidiano sportivo (modelli in `Testate/`, solo locali), dall'alto in basso:
  1. Testata con orecchiette, poi la riga con data di uscita (il giorno dopo l'ultima partita), giornata e girone.
  2. Sopratitolo: etichetta ciano (`occhiello`) più una riga che dà il fatto e il suo dato (`sopratitolo`).
  3. Titolone: una o due parole, in bastone stretto, a tutta riga. Il gioco di parole va sul blocco ciano. Il corpo si adatta da solo: se il titolo sta su una riga la riempie, altrimenti va su due.
  4. Catenaccio: una o due righe in grassetto con grazie, con il rimando "pag. 01" all'apertura.
  5. Apertura: foto con il punteggio della partita simbolo nel riquadro navy e la didascalia. Accanto c'è la spalla con il dato della giornata e la classifica sintetica (primi 5).
  6. Tabellino: tutti i risultati della giornata su fascia navy.
  7. Taglio basso: tre richiami alle pagine interne, ciascuno con occhiello, titolo, una riga e il numero di pagina. Contiene gli articoli dal secondo in poi; se gli articoli sono pochi, completano le rubriche.
  L'apertura della prima pagina è sempre il primo articolo dell'uscita.
- **Un file HTML per ogni articolo** (`01-...html`, `02-...html`, ...): ogni pagina contiene un solo pezzo e deve essere leggibile e completa da sola, perché verrà pubblicata come storia. Il numero del file è il numero di pagina richiamato in prima. Dall'alto in basso:
  1. Testata ridotta, poi la testatina: numero di pagina su navy, sezione su ciano (`sezione`, di base "La giornata"), giornata e data.
  2. Occhiello ciano, titolo in bastone stretto (una riga se ci sta, altrimenti due), catenaccio in grassetto (`sommario`).
  3. Firma ("di Redazione", oppure `firma`) e girone tra due filetti.
  4. Facoltativi: foto con didascalia (`immagine`, `didascalia`) e tabellino della partita su navy (`partita`, indice in `risultati`).
  5. Testo su due colonne con capolettera e quadratino di chiusura. Una `citazione` facoltativa va dopo il secondo capoverso, solo con parole dette davvero.
  6. In fondo, facoltativo, il box dei numeri (`numeri`: etichetta, valore, testo), solo con dati veri.
  Un pezzo troppo lungo per una pagina si divide in articoli consecutivi con `parte` 1, 2, ...: le pagine si richiamano da sole con "continua a pag." e "segue da pag.".
- **La cronaca di Gianluca Zanni** (`"tipo": "cronaca"`, `"firma": "Gianluca Zanni"`): pagina articolo con sezione "La nostra partita", occhiello "La cronaca", firma "La cronaca di Gianluca Zanni" con il nome su blocco rosa e il tabellino della nostra gara messo in automatico. **Colore della rubrica:** il rosa della maglia del portiere (`ROSA` nel generatore, #EC78C0), che su questa pagina prende il posto del ciano in testatina, occhiello, gioco di parole e firma; testata e firma in basso restano quelle di sempre. Anche l'occhiello del suo richiamo in prima è rosa (deciso da Nicola il 3 novembre). In prima pagina il richiamo riporta "di Gianluca Zanni". Regole al punto 8.
- **Rubriche fisse** (confermate), presenti in ogni uscita e ciascuna in un file proprio, con la stessa testatina e lo stesso schema di titoli degli articoli:
  - classifica, con sopra i numeri calcolati dalla classifica (capolista, posizione nostra e distacco, miglior attacco, miglior difesa) e la nostra squadra evidenziata;
  - risultati della giornata, con sopra i conti dei segni (gol, 1, X, 2) e per ogni gara punteggio, marcatori e probabilità pre-partita;
  - marcatori e assist, affiancati, con il primo (o i primi a pari merito) nel box ciano e le posizioni a pari merito;
  - prossimo turno, con le probabilità pre-partita quando disponibili.
  - **la partita della settimana** (decisa da Nicola il 3 novembre, precisata lo stesso giorno): un trafiletto di due o tre capoversi sulla gara più combattuta della giornata appena giocata, con il blocco della gara (punteggio, marcatori, probabilità della vigilia) e i numeri (posizione e punti di oggi delle due squadre, probabilità del pareggio). In fondo, facoltativo, lo spoiler sulla partita della settimana del prossimo turno (`prossima`: una riga). La gara la sceglie il generatore (`scegli_partita`): con le probabilità vince la più equilibrata (scarto più piccolo tra vittoria in casa e in trasferta); a parità o senza probabilità, la coppia più in alto in classifica, poi la più vicina in punti. Può essere anche la nostra gara. La scelta si forza con `indice` (risultati) e `indice_prossima` (prossimo turno). Il testo si scrive come gli altri (skill di giornalismo, poi humanizer) e resta sull'attualità; lo spoiler non fa pronostici.
  La nostra gara è segnata con la fascia ciano a sinistra e l'etichetta "La nostra gara".

Regole comuni a tutti i file:
- Stessa testata, stessi font, stessa palette e stessa griglia in ogni file e in ogni uscita, così le pagine sono riconoscibili come famiglia.
- Dimensione e proporzioni pensate per l'esportazione nelle storie: formato verticale 9:16 (confermato da Nicola), per esempio 1080x1920 px. Il testo deve stare nella pagina senza scorrere: se un pezzo è troppo lungo, accorciarlo o dividerlo in due pagine numerate.
- Ogni file HTML è autonomo (CSS incluso, nessuna dipendenza esterna che si rompa all'esportazione).
- Curare sempre l'impaginazione con la skill UI-UX Pro: gerarchia tipografica, spaziature, contrasti, leggibilità su telefono. Applicarla a copertina e articoli prima di consegnare.

- **Firma e copyright in ogni pagina:** ogni file HTML riporta sempre, in posizione fissa e ben visibile ma elegante (per esempio in basso o in verticale sul bordo), la dicitura di copyright con il nome degli autori e creatori del giornale, tra virgolette, più il nome della testata e il numero dell'uscita. Serve a rendere riconoscibile la paternità di ogni pagina, anche se ne viene fatto uno screenshot e ripubblicato. Mai omettere la firma, mai nasconderla o renderla illeggibile. Si può aggiungere un elemento grafico distintivo ricorrente (marchio, filetto, sigillo) che sia parte dell'impaginazione e non facile da ritagliare.

Stile grafico: quotidiano sportivo online contemporaneo, con titoli forti, tipografia con grazie per i testi e carattere deciso per i titoli. Palette fissa: sfondo bianco e testi blu navy. Terzo colore per i blocchi (riquadri, pannelli, evidenziazioni): azzurro ciano, usato sempre allo stesso modo in tutte le pagine e in tutte le uscite. Nessun altro colore. Eccezioni: il rosa della rubrica di Zanni (vedi sopra), solo nella sua pagina e nel suo richiamo in prima; i loghi ufficiali delle squadre (cartella `logo/`), che il generatore mette piccoli accanto ai nomi in classifica, risultati, prossimo turno, tabellini e riquadro del punteggio in prima, con i loro colori originali. Testata e logo originali: non riprodurre loghi o grafica di testate esistenti.

Già deciso:
- Testata: quotidiano classico con doppi filetti, "La Gazzetta del DRAGONE", testa del drago (richiamo IMPLAST) nell'orecchietta sinistra su blocco ciano, numero dell'uscita in quella destra. File e regole in `assets/logo/`.
- Nome della testata: "La Gazzetta del Dragone"
- Firma in ogni pagina: "© Redazione La Gazzetta del Dragone, tutti i diritti riservati", con numero dell'uscita
- Palette: sfondo bianco, scritte blu navy, terzo colore per i blocchi azzurro ciano
- Rubriche fisse: classifica, risultati, marcatori e assist, prossimo turno, partita della settimana
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
- **Humanizer sempre** (regola fissata da Nicola il 3 novembre): ogni testo scritto da Claude passa nella skill `humanizer` prima di essere consegnato o impaginato. Vale per tutto: articoli, titoli e titoloni, catenacci e sommari, occhielli, didascalie, richiami in prima, box dei numeri, testi delle rubriche, proposte di titolo. Humanizer non cambia i dati: dopo il passaggio ricontrollare che cifre, nomi e fatti siano identici a prima. Unica eccezione: la cronaca di Gianluca Zanni, che non si tocca.
- Consegnare i testi anche in un file `.md` pulito, senza HTML, separati per articolo, con titolo e sommario.
- **Articolo davanti al nome delle squadre** (regola di Nicola, 4 novembre): la Cazzaghese, unica squadra femminile del girone, vuole il femminile ("la Cazzaghese"); tutte le altre il maschile ("il Giaffa", "il Bombetta", "l'Implast").
- Tono di default: da quotidiano sportivo, vivace ma preciso. Cambiare solo su richiesta.
- **Mai pezzi piatti (richiesta esplicita di Nicola).** Un articolo che riporta solo risultato e marcatori è da rifare. Ogni pezzo deve avere una tesi, una lettura dei fatti che il lettore non trova sul tabellino. Per esempio: perché una squadra è prima senza essere la migliore in nessuna voce, cosa racconta una serie, quale partita ha cambiato il senso di un'altra. Lo sviluppo deve essere articolato: un'apertura che entra nella storia, i numeri messi al servizio dell'idea, un confronto con le giornate precedenti, una chiusura che lascia una domanda aperta per le prossime uscite. La fantasia sta nell'angolo, nella struttura, nelle immagini e nel lessico. I fatti restano solo quelli dei dati (punto 3): niente scene, frasi o emozioni inventate attribuite a persone reali.

### La cronaca di Gianluca Zanni
Le nostre partite le racconta Gianluca Zanni, giornalista della redazione, con un pezzo firmato in ogni uscita in cui giochiamo.
- Il testo è suo: Nicola lo passa e Claude lo impagina così com'è. Claude non lo scrive, non lo riscrive, non lo accorcia e non lo passa in Humanizer (nel file `.md` è segnato apposta).
- Claude controlla le cifre del pezzo (risultato, marcatori, minuti) con lo storico dei dati. Se qualcosa non torna lo segnala a Nicola, senza correggere da sé.
- Titolo e sommario: quelli di Zanni, se li ha dati. Altrimenti Claude ne propone due varianti e Nicola sceglie.
- Se il pezzo non sta in una pagina, si divide in due parti (`parte` 1 e 2), mai tagliando il testo.
- Gli articoli della redazione non rifanno la cronaca della nostra partita: la danno per letta e, se serve, rimandano alla pagina di Zanni. Prendono altri angoli (punto 5).
- Mai attribuire a Zanni frasi, giudizi o citazioni che non ha scritto.

## 9. Continuità
- Prima di scrivere una nuova uscita, rileggere questo file e l'uscita precedente.
- Mantenere la memoria della stagione: sorpassi, serie in corso, promesse lasciate in sospeso ("vedremo se..."), da riprendere nelle uscite successive.
- Se qualcosa cambia nelle regole, aggiornare questo file e segnalarlo a Nicola.

## 10. Strumenti già pronti nel progetto
- `template/genera_uscita.py contenuti/giornata_XX.py`: genera le pagine HTML 9:16 (copertina, articoli, rubriche) con testata, firma, firma verticale sul bordo e filigrana del drago in ogni pagina, più `uscite/giornata-XX-articoli.md` con i testi puliti. Font di sistema: Georgia per i testi, Franklin Gothic Demi per titoli e numeri (le cifre di Georgia sono "all'antica" e lo 0 sembra una o).
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
