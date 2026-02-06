# Stato dell'arte del progetto

## 06-02-2026

Allo stato attuale, la realizzazione del progetto è arrivata a questo punto:

### Database

Si è optato per il database sqlite3 con l'aggiunta della libreria per il campo vettoriale.

Allo stato dell'arte sono definitive le seguenti tabelle:
- users
- documents (per il salvataggio del dato relativo al file)

Il resto è in fase di revisione.

**Pensiero**

La divisione proposta dall'AI tra la tabella dei chunk e la tabella degli embed è interessante, ma al di fuori che la seconda è necessaria per via del campo di tipo *vettoriale*, la prima va un pò rivista, in quanto ancora non mi è chiaro benissimo, come fare la trasformazione *chunk versus embed*.

### Gestione tabelle e action in query

Per il momento è stata creata:

- la classe per la connessione, che restituisce il cursore
- la classe generica con le *action*, per le query
- i seguenti model:
  - users
  - documents ( solo insert )
 
Il resto va ancora fatto.

In merito non ci sono dubbi.


### Strategie di chunk

Si sono definite le varie strategie che verranno mappate saggiamente nel db (anche per usare come filtro per ottenere i dati di confronto).
Al momento resta da valutare cosa usare per i file world e PDF.

Il resto è presente, ma deve essere testato e valutato.

### Embedfing

Al momento ho previsto un servizio, che ( da provare), fare i jobs come definito nel paragrafo **Idee**.

Al momento ci sono più dubbi che soluzioni, soprattutto legate alle prestazioni, visto che passare n chunk e quindi chiamare n volte la stessa api (*Ollama Embeding*), mi genera un po' di preoccupazione.

Vedremo nei prossimi giorni.

### Valutazioni

#### Valutazione dei chunk

Allora ho creato l'api per caricare attraverso postman, una serie di file di diversa natura.
Ora anche quì mi è nato il dubbio se farò partire subito la chunk, come definito sopra o passarla a uno scheduler/worker che opera in maniera asincrona.

Resta poi da capire, una volta caricati una serie di file se e come dire se la divisione sia o meno accettabile.

*Va definito uno standard di valutazione*

#### Valutazione modello

Ancora nessuna idea portata avanti.


### Api e sicurezza delle api

Lato sicurezza ho creato il classico jwt. Per il momento va bene, bisogna farlo valutare dall'AI se avesse maggiori suggerimenti in merito.

Le api di user ( registrazione,login e aggiornamento password) sono presenti.

Esiste l'api di caricamento file, che allo stato attuale carica i dati sul db(*tbl documents*) e carica il file nella directory **import-data** .

Il resto delle api sarà fatto man mano che si procede con la realizzazione della parte chunk,Embeding e chat.

### Fe

Ultima cosa che faccio o faccio fare dall'Ai.

### Altre gestioni

Nel file di Embeding service ho già gestito l' eventualità che il task finisca, ma devo rivederlo.

---


## Idea da appuntare

Si potrebbe salvare la ripartizione del file nella tabella X con un campo *is_converter*, posto a false; attraverso uno scheduler che gira ogni ora e attraverso le code andare lato db ( attraverso la query 
```
select * from X where is_convert =false;

```
vedere quelle da convertire in embed ( fatto in maniera asincrona )

---

## Prossimi passi

Continuare il caricamento dei file e trovare la soluzione migliore per la divisione del contenuto in chunk.
Quindi trovare uno standard di valutazione ( domandare all'AI).
