# Introduzione della rag nel progetto

Obiettivo è quello di caricare dei documenti (testo), legato sempre all'argomento del modello, per poter dare un supporto e far capire la *previsione finale* perchè sia quella.

## Passaggi

1. cercare i file e selezionare quelli più pertinenti all'argomento del modello
2. estrarre il contenuto dei file (in formato .txt, .md, .csv, .json, .pdf)
3. dividere il contenuto in chunk (paragrafi)
4. trasformare i chunk in vettori usando ollama
5. salvare i vettori in un database (*per il momento mantangeno il postgress attuale senza la libreria per vettori*)
6. alla domanda: trasformare la domanda in vettore usando ollama
7. confrontare il vettore della domanda con i vettori dei chunk tramite cosine similarity (*da creare lato codice*)
8. recuperare i Top-K chunk e passarli a ollama per la risposta (*da creare lato codice*)

## Note

- i file da caricare sono sempre legati all'argomento del modello
- i file sono in formato .txt, .md, .csv, .json, .pdf
- i chunk sono sempre paragrafi
- i vettori sono sempre float64
- la cosine similarity è sempre tra 0 e 1
- i Top-K chunk sono sempre 3