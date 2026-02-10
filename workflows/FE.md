# Realizzazione del Front End

Il front end è realizzato con Vue e PrimeVue.

Dovrà essere inserito in una rotta che restiuisce un template html.

## Cosa deve contenere

- Login classica (username e password)
- Home (al momento vuota)
- una parte amministratore
- una parte utente

Per adesso realizzerò a fini di valutazione dei *chunck e dei embeddings* solo la parte di **amministratore**.

## Condizioni

Quando viene aperta la parte FE, il sistema verifica se esiste un token (*jwt*), valido; se non esiste o scaduto, il sistema reindirizza alla pagina di login.

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