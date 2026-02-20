# Realizzazione del Front End

Il front end è realizzato con Vue e PrimeVue.

Dovrà essere inserito in una rotta che restiuisce un template html.

## Cosa deve contenere

- Login classica (username e password)
- Home (al momento vuota)
- una parte amministratore
- una parte utente

Per adesso realizzerò a fini di valutazione dei _chunck e dei embeddings_ solo la parte di **amministratore**.

## Condizioni

Quando viene aperta la parte FE, il sistema verifica se esiste un token (_jwt_), valido; se non esiste o scaduto, il sistema reindirizza alla pagina di login.

Se esiste e valido, il sistema reindirizza alla pagina di home.

Se lo usernmame è **admin**, il sistema reindirizza alla pagina di amministratore.

Se lo usernmame è diverso da **admin**, il sistema reindirizza alla pagina di utente.

Quindi a seconda del ruolo,non solo il sistema reindirizza alla pagina corrispondente, ma sarà presente un menù diverso.

## Pagine

### Login

Deve contenere un form con due campi: username e password.
Al click del bottone **Login**, il sistema verifica le credenziali, chiama l'api di login ( come da file [server.py](server/server.py))

I due campi sono obbligatori.

### Home

Nella home deve essere previsto al momento un solo messaggio, senza alcun link. Sarà presente un menù con le seguenti voci:

- Amministratore
- Utente
- Logout

Il messaggio sarà: **Benvenuto in NexusTag-AI - AMMINISTRATORE ** se l'utente è admin, **Benvenuto in NexusTag-AI - UTENTE ** se l'utente è utente.

### Amministratore

1. lista dei documenti
2. lista dei chunck per il documento x selezionato

Queste pagine devono contenere una tabella con i dati.
I campi di questa tabella sono recuperabili dal file dello schema del db ([schema.sql](database/schema.sql))

Per il momento devo creare le api per recuperare i dati.

Le tabelle saranno di tipo **datatable-server**, con la paginazione e il filtro gestiti dal server, l'ordinamento e la ricerca gestiti dal client.

Ogni volta che cambia qualcosa il sistema, dovrà richiamare l'api per recuperare i dati, con i parametri corretti.

## Utente

Per il momento non implementare la parte utente.

## Colori e temi

I colori e i temi sono definiti come segue:

- **primary**: #007bff
- **secondary**: #6c757d
- **success**: #28a745
- **danger**: #dc3545
- **warning**: #ffc107
- **info**: #17a2b8
- **light**: #f8f9fa
- **dark**: #343a40

Usare il theme chiaro e uno sfondo neutro.

## Aggiornamenti UI e Funzionalità Recenti

### Design e User Experience

L'interfaccia è stata evoluta per offrire un'esperienza premium e altamente leggibile:

- **Tema Adattivo**: Implementato un sistema di colori basato su variabili CSS che supporta nativamente la **Dark Mode**. Lo sfondo del body utilizza un grigio ardesia morbido (`#1e293b`), mentre le tabelle utilizzano un effetto _glassmorphism_ per staccarsi visivamente dal fondo.
- **Tabelle Avanzate**:
  - Introdotto lo **Zebra Striping** (righe alterne colorate) per facilitare la lettura dei dati.
  - Header e Footer delle tabelle hanno uno sfondo contrastato (`#020617`) per incorniciare il contenuto.
  - I pulsanti di azione sono stati snelliti (rimosso il testo, mantenuta l'icona con tooltip) per ridurre il carico visivo.
- **Navigazione Contestuale**: La pagina dei chunks ora visualizza dinamicamente il **nome del file** nell'intestazione (passato tramite query parameters) invece del semplice ID numerico.
- **Search Bar Moderna**: Gli input di ricerca globale integrano l'icona all'interno del campo di testo per un look più pulito.

### Sicurezza e Gestione Stato

- **Navigation Guard (beforeEach)**: Il router è stato blindato. Al primo accesso o al refresh, se il token JWT non è presente o è invalido, l'utente viene reindirizzato immediatamente alla Login, impedendo la visualizzazione della Home anche solo parzialmente.
- **Pinia Store**: Lo stato dell'autenticazione è gestito centralmente. Il token e i dati utente sono sincronizzati con il `localStorage` per mantenere la sessione attiva.
- **Intercettori Axios**: Ogni chiamata API in uscita inietta automaticamente l'header `Authorization: Bearer <token>`. In caso di errore 401 (token scaduto), il sistema effettua il logout automatico e riporta alla login.

### Gestione Documenti (Upload)

Aggiunta una nuova sezione amministrativa per l'acquisizione di file:

- **Gestione File**: Supporto per estensioni multiple (`txt`, `pdf`, `csv`, `docx`, `xlsx`, ecc.) con validazione lato client.
- **Topic Matching**: Durante l'inserimento dell'argomento, il sistema effettua una ricerca in tempo reale (on-change) suggerendo i topic già presenti nel database per prevenire duplicati e incoerenze.
- **Integrazione API**: Il caricamento utilizza l'endpoint dedicato `/api/auth/upload_file` con gestione multiparte per file e metadati.

### Internazionalizzazione (i18n)

Il portale è ora accessibile a un pubblico globale:

- **Multilingua Nativo**: Integrazione di `vue-i18n` con supporto per **Italiano** e **Inglese**.
- **Switch Dinamico**: Implementato un selettore di lingua nella barra di navigazione e nella pagina di login per cambiare il locale dell'intero portale senza ricaricare la pagina.
- **Localizzazione UI**: Tutte le etichette, i messaggi di errore, i titoli delle colonne e i feedback di sistema sono mappati tramite chiavi di traduzione.

### Architettura e Refactoring

- **Incapsulamento Modelli**: La logica di suggerimento dei topic è stata spostata dal controller (`server.py`) direttamente nella classe `Documents` del backend.
- **Ereditarietà**: Il nuovo metodo di ricerca utilizza le funzioni di base della classe `ModelGeneral`, garantendo una gestione più robusta e riutilizzabile delle query SQL.

- **Internazionalizzazione Integrale**: Estesa la localizzazione anche alla pagina di Login (con switcher dedicato) e alla Home, completando la copertura multilingua di tutte le sezioni amministrative.

### Pagina di Login

- **Redirezione Unificata**: Una volta effettuato l'accesso, indipendentemente dal ruolo, l'utente viene indirizzato alla pagina **Home** per garantire un punto di partenza coerente e familiare.

## Area Utente e Gestione Avanzata Elaborazione

L'ultima evoluzione ha introdotto una netta separazione dei ruoli e una gestione asincrona dei carichi di lavoro:

### Area Utente

- **Filtro Proprietario**: Gli utenti non-admin hanno un'area dedicata dove visualizzano esclusivamente i documenti da loro caricati.
- **Accesso Upload**: Anche gli utenti standard possono caricare documenti, la cui elaborazione è però delegata allo scheduler notturno.

### Elaborazione Manuale (Admin)

- **Workflow Asincrono**: L'avvio dell'elaborazione (tramite la nuova icona **Play**) utilizza `BackgroundTasks` lato backend. Il server risponde immediatamente, evitando timeout su file di grandi dimensioni.
- **Polling dello Stato**: Il frontend monitora lo stato del documento tramite un'API di status dedicata, aggiornando l'interfaccia non appena il processo è terminato.
- **Freeze del Portale**: Durante l'elaborazione, l'interfaccia viene bloccata con un overlay e una `ProgressBar` per indicare il progresso e prevenire azioni incrociate.
- **Feedback Errori**: Il sistema ora riporta messaggi di errore specifici provenienti dalle API direttamente nei toast di notifica, facilitando la diagnosi di eventuali problemi.

### Scheduler Notturno

- **Esecuzione Ottimizzata**: Lo scheduler automatico si attiva periodicamente (configurato per intervalli) per processare i file in coda senza intervento manuale.

### Monitoraggio Scheduler e Feedback Utente

L'intero ciclo di vita dell'elaborazione è ora trasparente per l'utente e monitorato globalmente:

- **Stato Documento**: Per i file appena caricati (stato `uploaded`), è stata aggiunta una nota informativa: _"File in attesa di elaborazione da parte dello scheduler"_. Questo chiarisce all'utente che non deve agire manualmente.
- **Badge Globale (Navbar)**: Lo stato dello scheduler è stato spostato nel layout principale (`DefaultLayout.vue`), rendendolo visibile in **tutte le pagine** per l'amministratore.
  - Un **countdown in tempo reale** (minuti:secondi) alla prossima esecuzione prevista.
  - Un'animazione di **"Esecuzione in corso"** quando il sistema sta effettivamente processando i file.
- **Architettura Global Store (Pinia)**: Implementato `useSchedulerStore` per gestire centralmente il polling verso l'API `/api/jobs/status`, garantendo che i dati dello scheduler siano coerenti e disponibili ovunque nel frontend.
- **Infrastruttura di Monitoraggio Backend**: Implementato un singleton nel backend e un'API dedicata per sincronizzare lo stato dello scheduler con il frontend.
- **Internazionalizzazione**: Tutte le stringhe relative allo scheduler (note di attesa, countdown, stati) sono state localizzate in Italiano e Inglese.
- **Design Premium**: Il badge globale utilizza icone dinamiche (orologio/spinner) e un font monospace per una leggibilità ottimale del timer.

### Monitoraggio Fallimenti (Job Failed Logs)

Per una diagnosi completa del sistema, è stata introdotta una gestione centralizzata degli errori:

- **Pagina Log Errori**: Una nuova sezione amministrativa ("Job Falliti") elenca tutti i problemi riscontrati dallo scheduler durante l'elaborazione.
- **Dettagli Eccezioni**: La tabella mostra l'ID del documento, la riga del processo e l'eccezione riscontrata. Cliccando sull'errore, si apre un dialog con il trace completo del problema.
- **Integrazione API**: Nuovi endpoint lato backend permettono di consultare lo storico dei fallimenti con paginazione server-side.
- **Tracciabilità**: Ogni errore è collegato al documento originale, permettendo all'amministratore di capire esattamente cosa ha causato il blocco e intervenire.
