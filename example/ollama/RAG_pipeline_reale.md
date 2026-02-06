# RAG (Retrieval-Augmented Generation) – Pipeline “Reale” e Principi di Sistema

Questo documento descrive **come funziona una RAG in un contesto reale**, dal punto di vista ingegneristico, senza confondere **AI**, **parsing**, **storage** e **retrieval**.

---

## 1. Principio fondamentale

> **Una RAG non è un modello.**  
> È una pipeline di trasformazione dell’informazione.

Il modello (LLM) **non contiene conoscenza**.  
La conoscenza è “caricata” nel sistema attraverso un processo di normalizzazione e indicizzazione.

---

## 2. Cosa deve saper fare un sistema RAG reale

### 2.1 Accettare input eterogenei
Il sistema deve poter ricevere file di diversi formati:

- PDF
- DOCX
- TXT
- HTML
- CSV
- Email
- ecc.

Ogni formato ha struttura diversa e rumore diverso.

---

### 2.2 Estrarre il contenuto semantico
Il sistema deve **estrarre testo pulito** mantenendo:

- paragrafi
- titoli e sottotitoli
- elenchi
- separazione logica tra sezioni

Questa fase è **information extraction**, non AI.

---

### 2.3 Chunking intelligente (cuore del sistema)
Il chunking deve:

- rispettare unità logiche
- evitare frammentazione
- evitare aggregazione eccessiva
- usare overlap dove serve

> Il criterio è epistemologico:  
> **“Questo pezzo può rispondere a una domanda?”**

**Chunk ≠ pagina**  
La pagina è un concetto tipografico, il chunk è un concetto semantico.

**Regole pratiche:**
- dimensione: 200–500 parole (o 500–1000 token)
- overlap: 10–20%
- unità: paragrafi, sezioni, sottosezioni

---

### 2.4 Generare embedding coerenti
Per ogni chunk:

- testo pulito
- contesto sufficiente
- dimensione controllata

L’embedding è un vettore numerico che rappresenta il significato semantico del chunk.

---

### 2.5 Persistenza della conoscenza (DB)
Il database non è un dump: deve permettere:

- ricerca per similarità
- tracciabilità (file, sezione, pagina)
- ricostruzione del contesto

**Campi minimi consigliati per ogni chunk:**

| Campo | Descrizione |
|------|-------------|
| `file_id` | identifica il documento di origine |
| `chunk_id` | identificatore del chunk |
| `chunk_text` | testo del chunk |
| `embedding` | vettore numerico |
| `chunk_index` | ordine nel documento |
| `metadata` | pagina, sezione, ecc. |

---

### 2.6 Recupero e risposta (query time)
Quando arriva una domanda:

1. Converti la domanda in embedding
2. Confronti l’embedding della domanda con quelli dei chunk
3. Recuperi Top-K chunk più simili
4. Passi la domanda + contesto (Top-K) al modello LLM per generare la risposta

---

## 3. Punto chiave

> **La qualità della risposta dipende più dal chunking che dal modello.**

Un modello mediocre con chunking eccellente può dare risposte migliori di un modello eccellente con chunking pessimo.

---

## 4. Formula mentale corretta

> **Il tuo sistema non “capisce tutto”.**  
> Ha solo reso interrogabile il sapere.

L’LLM:
- non conosce i file
- non conosce il DB
- risponde solo a ciò che gli dai come contesto

---

## 5. Traduzione tecnica della tua frase

> “Il sistema deve normalizzare qualsiasi fonte informativa in unità semantiche interrogabili, tali che il retrieval massimizzi la rilevanza rispetto alla query.”

---

## 6. Prossimi passi consigliati (da mondo reale)

- strategie diverse di chunking per tipo di file  
- gestione di documenti molto lunghi (libri, manuali)  
- come evitare risposte “quasi giuste” (hallucination)  
- come valutare se una RAG sta funzionando bene  
- scelta del DB vettoriale e performance di retrieval  

---

## 7. Nota finale

Una RAG efficace è un sistema di **pipeline**, non un singolo modello.  
La qualità dell’intero sistema dipende dalla capacità di:

- estrarre informazioni
- chunkare correttamente
- generare embedding coerenti
- recuperare il contesto giusto
- dare al modello LLM un contesto rilevante

---

