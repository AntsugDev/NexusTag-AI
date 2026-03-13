# Progetto Rag

Obiettivo di questo file è descrivere in dettaglio, quello che dovrei eseguire per raggiungere lo scopo.

## Scopo del Progetto

Il progetto deve prevedere un contenitore che può caricare dei documenti, di diversa natura e su questi fare domande(chat)
per ottenere risultati.


Per far questo i passaggi del sistema sono:

- caricamento dei documenti, a cui definire un tag di riconoscimento
- consultazione dei questi
- possibilità di porre delle domande (RAG), usando il tag come filtro
- valutazione dei risultati, con possibilità di un agente Ai su quest'ultimo
- testing

I passaggi sopra per essere realizzati, devo prevedere quanto segue:

1. scelta del database
2. scelta del linguaggio da usare per la parte Ai
3. scelta del linguaggio da usare per la parte api/Backend
4. scelta del linguaggio da usare per la parte Frontend

## Scelte linguistiche

### database

Per il database si è optato per un db *sqlite*, con l'aggiunta della parte vettoriale *vec_o*.
Il database dovrà contenere le seguente tabelle (almeno nella versione iniziale/base):

- **users**: tabella delle utenze
- **tags**: tabella tipologica per i tags usati per dividere i documenti in n categorie
- **documents**: tabella dei documenti caricati da quell'utenza
- **stato del file**: tiplogica che rappresenta lo stato del file (*caricato, lavorato, in attessa, errore, ecc,*)
- **chunks**: tabella che rappresenta la divisione in *chunks* del documento x e sarà legata a quest'ultima tabella
- **strategia chunks**: tabella che rappresenta le differenti tipologie che si possono adottare per dividereun documento
- **question**: tabelle delle domande effettuate dal quell'utenza
- **embending**: la tabella per la parte vettoriale, dove si avranno i chunks e/o le question
- **valutazione**: tabella che rappresenta le valutazioni fatte per i chunks, per i test, ecc.
- **jobs**: se verrà previsto uno scheduler o un azione automatizzata
- **failed_jobs**: per tener traccia di eventuali jobs non andati a buon fine

## linguaggio

In prima istanza si è pensato a **python**, visto chè questo ha a disposizione tante librerie, ma la versione attuale del progetto risulta caotica (anche per questioni temporali); 
pertanto si è provato con **laravel**, anche se andava sempre scritto qualcosa in python per mancanza di librerie.

Quindi soluzione migliore è il python, ma devo seguire uno schema ben preciso e salvare quello che c'è di buono nella versione precedente.

Lato Frontend sicuramente *vue, primevue e vuex*, ma come passaggio questa deve essere fatta per ultimo, prendendo le basi create nella versione precedente.

---

## Task

In questo paragrafo saranno definiti i passaggi da seguire, creando i task lato github per evitare passaggi inutili e che mi fanno perdere tempo.
Prima di procedere però definiamo la struttura.


La directory principale deve contenere:

- *main*, per la inizializzazione della parte python (server ede eventuali azioni)
- *.env*, con solo le variabili necessarie
- *envorement*, la directory con le librerie necessarie
- *libraries.txt*, la lista delle librerie da installare

Le directory da creare sono:

- *database*: per la gestione del database(connessione e creazione database)
- *models*: che deve contenere i file che rappresentano le tabelle con le colonne e le azioni possibilità
- *server*, che rappresenta la directory che deve contenere la parte relativa alle api; in questa ci devono essere:
   - *controller*: gestione separata delle api (con tag, descrizione e path diverso)
   - *request*: (BaseModel), per la gestione dei payload per le richieste
   - *auth*: per la gestione del jwt per le api
- *chunks*, che deve contenere le strategie di chunks
- *embending*, per la gestione dell'embending
- *chat*, per la gestione della chat(da vedere se necessaria o se si chiamano le api) 
- *utility*, per i file common che si potrebbe avere  

**NOTA**: per ogni file creato deve essere esplicitamente fatto un test di funzionamento

## Task 1 - Creazione e gestione del db

Questa parte deve prevedere la creazione del db e la gestione della connessione ad esso, nonchè il popolamento delle tipologiche.

**Passaggio 1:** definizione dello schema e delle relazioni
**Passaggio 2:** creazione del file per la connessione (dentro la directory **database**) e la gestione della migrazione dei dati
**Passaggio 3:** creazione dei models (nella directory **models**), secondo le colonne della tabella

Il file generale del model deve prevedere le funzioni:

- index: lista 
- store: la creazione
- update: la modifica
- delete: la cancellazione
- find: per la ricerca del dato from id
- findBy: per la ricerca del dato secondo una colonna predefinita
- stamtement: per una ricerca del dato più dettagliata e libera
- paginazione, per le tabelle

Deve essere revisionato la parte del fetch, in modo tale che ogni volta non devo ammazzarmi a capire, come convertire il dato.

> query create secondo sopra, execute con il *row factor*, return fetchAll gestito ad alto livello ( in generale)

In pratica:
- insert deve ritornare l'*id* inserito
- update/delete deve ritornare true o false
- il resto il fetch all

## Task 2 - Definizione del server

In questo task deve essere definito il *server* (FastApi e unicorv) e deve essere definita la strategia di auth.

Quindi, il file base del server deve contenere:

- l'inizializzazione
- la definizione della rotta base
- la definizione di un api per vedere il corretto funzionamento ( **healt-check**)
- la creazione dei controller con le proprie rotte, man mano che vengono creati

In questa fase deve però essere creato solo la *base*.

Una volta terminato aggiungere l'avvio nel *main* e testare il funzionamento del server


## Task 3 - Login e Registrazione

Prevedere il controller e le request per la creazione di un utenza e per la login con l'ottenimento del jwt token necessario alle future chiamate api
Una volta creata va inclusa nel file server e testata.

## Task 4 - Caricamento e lettura dei documenti

In questo task deve essere previsto la creazione dell'upload del documento nonchè la sua visualizzazione(Globale o Singola);
Una volta creata va inclusa nel file server e testata.


## Task 5 - Creazione dei chunks

Questo task viene diviso in piccoli task:

### Task 5.1 - Creazione delle strategie di chunks
In questo Task deve essere previsto la creazione, in base al file, della lettura e divisione del file.

I passaggi sono questi:

- Carico il file
- leggo il file e individuo l'estenzione
- divido in chunks

La seconda parte, può essere fatta da un file common che prende e legge l'estenzione ed in base a quella ripartisce chi dovrà fare cosa.
In questo file, quindi, si deve aspettare l'id del documento e la posizione o il base64( il contenuto) di questo;
tutto ciò verrà passato al relativo chunks.

Per il momento partiamo dai seguenti file:

- text
- log
- sql
- json
- markdown
- php (bisogna vedere)

Questo task è il primo dei fondamentali.

Per ogni strategia usata fare n test, per vedere se è tutto ok.

### Task 5.2 - Creazione delle api

Vanno create le seguenti api:

- se non si usa lo scheduler, l'api di avvio per quel documento
- se si usa lo scheduler, l'api che cambia lo stato del documento e lo scheduler farà quanto nel task sopra
- l'api della lista dei chunks, dato quel documento(paginata)

La scelta tra le prime due dipende dalle tempistiche.

Alla fine di tutto includere ciò nel file server e testare n volte.


**NOTA**:

Quì si apre una fase importante.
*Fare si o no direttamente i vettori per ogni chunk?*

Dipende dai tempi.

Quì ci sono varie possibilità:

1. usare le funzionalità di ollama/langchain
2. usare le api di ollama/langchain

## Task 6 - creazione embending

Per questo devo fare delle valutazioni in merito su come agire

## Task 7 - creazione della domanda

Creare il controller e la request, per inserire una domanda che si vuole fare.
In questo caso deve essere creato direttamente il vettore e inserito nel db, nelle due tabelle.
Creare una lista delle domande fatte.
Creare una storicità (*questo punto è da valutare come*, ad esempio lato Fe usare il vuex e poi passare tutto al db per la storicità); in questo caso in tabella deve essere previsto un order e una data (no created_at)

Unire il tutto al server e testare

## Task 8 - La chat
Questa parte devo ancora valutarla


Questi sono i task lato Backend.

---
---




