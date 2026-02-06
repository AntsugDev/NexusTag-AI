# Esecuzione dei task per la creazione della rag

## Fase 1: Studio della realizzazione di un modello di embedding

In questa fase, lo scopo è quello di realizzare un modello di rag, secondo quanto previsto nel file [Rag](rag.md)

### Task 1: La logica

La logica è stata affrontata e si sono capiti i passagi da realizzare. Di seguito quanto:

- creazione del database e dei modelli per la gestione delle query
- creazione delle *strategie di chunck*, per le diverse tipologie di file
- creazione del modello di embedding
- creazione dei test per la verifica del modello
- gestione degli errori
- creazione della api
- creazione della parte FE
- docker o similare

Questi sono i task che si sono affrontati e si sono capiti i passaggi da realizzare.

## Fase 2: Realizzazione del modello di embedding

In questa fase, lo scopo è quello di realizzare un modello di rag, secondo quanto previsto nel file [Rag](rag.md)

### Task 1:creazione del database e dei modelli per la gestione delle query

Il database è stato creato in *sqlite*, secondo il file [schema.sql](rag\database\schema.sql).

Allo stato attuale, il database contiene le seguenti tabelle:
- users
- documents
- chunks
- embeddings
- queries
- results
- chunk_usage
- rag_runs
- jobs_failed

Queste sono in fase di revisione , in quanto nel creare *chuncking/embedding* si sono presentati diversi problemi.

### Task 2: creazione delle strategie di chunck

Le strategie di chunck sono state create in base alla tipologia di file. Di seguito quanto:
- txt
- log
- md
- sql
- csv
- xls
- xlsx
- pdf
- doc
- docx
- docs
- generic

Le strategie sono espresse seul file **.env**

Allo stato attuale, resta la valutazione dei file di tipo *world e pdf*.

### Task 3: creazione del modello di embedding

Ho creato un modello di embedding utilizzando *ollama* e *langchain_ollama*(in alcuni casi).

Per il momento non è terminato, in quanto sto rivedendo il database e le strategie di chunck.


### Task 4: creazione dei test per la verifica del modello

Questo task non è ancora in fase di studio.

Sicuramente andrò a creare per i file testuali una cosa simile a questa:

```
Estraggo dal testo una serie di frasi e provo ripetutamente a porle come domande; in seguito verifico se la risposta del modello è corretta e se è sempre la stessa e faccio statistica in merito.

```
A grandi linee può essere utilizzato anche per i file *world e pdf*, quanto sopra.

Per i file di natura tabellare, utilizzerò un approccio diverso,tipo questo:

```
Estraggo le righe e le colonne e i nomi e la tipologia del campo, e provo a domdare il max o il min (se fossero numeri) o colori oppure testo
```

In generale, userò comunque strumenti e librerie già esistenti per creare i test. (**Da studiare**).

### Task 5: gestione degli errori

Ancora in fase di studio.

### Task 6: creazione della api

La base delle api è stata creata in *fastapi*.

Per il momento non è terminato, in quanto sto rivedendo il database e le strategie di chunck.

Al momento sono presenti solo le api legate alla login e registrazione.

Da valutare se usarle direttamente o se dividere questo progetto con la parte FE, realizzando attraverso **laravel-vue** la parte BE/FE, in modo tale da tenere nascoste le api originali; in questo caso, andrebbe creata un *api-key* per utilizzare le api originali.



### Task 7: creazione della parte FE

Ancora in fase di studio.

### Task 8: docker o similare

L'idea sarebbe quella di creare un container globale, dove si troverebbe:

- agente ai / rag
- api
- parte FE
- database

Deve essere valutata, se su può installare **Ollama**, all'interno del docker e come e se il container stesso a questo punto funziona.

Oppure, al di fuori del docker, prevedere una soluzione alternativa (*ma ancora in fase di studio*)


