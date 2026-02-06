# Spiegazione ollama e rag

**La mia domanda:**

> quindi per vedere se ho capito: tanti documenti carico sul db vettoriale(per quell'argomento), questi poi li passo a ollama, pongo la mia domanda e lui trova la similarità con i vettori che ho nel db

**La risposta:**

> Carico molti documenti nel DB vettoriale.Quando pongo una domanda, il sistema calcola l’embedding della domanda, cerca i vettori più simili nel DB, recupera quei testi e li passa a Ollama insieme alla domanda.

<pre>
Documento
↓
Chunking
↓
Embedding (model embed)
↓
Salvataggio nel DB vettoriale

</pre>

**Ollama può essere usato solo per creare embedding, ma:**

- non li memorizza
- non li confronta

<pre>
Domanda utente
↓
Embedding della domanda
↓
Similarity search (vector DB)
↓
Recupero TOP-K chunk
↓
Prompt = domanda + chunk trovati
↓
Ollama (LLM) genera risposta

</pre>

_“In una RAG il modello non accede ai dati.
Il sistema calcola embedding per documenti e query, usa un DB vettoriale per la similarità, e passa solo i contenuti rilevanti al modello per la generazione.”_

Ollama serve per due cose distinte

1. Generare embedding (vettori)
2. Generare testo (risposte)

E nella RAG tu userai entrambi, ma in momenti diversi.

## Fasi uso ollama in una RAG

Quindi la pipeline completa è:

1. Ingestione documenti (una volta)

- Prendi i documenti
- Li trasformi in vettori con Ollama
- Li salvi nel vector DB

2. Query (ogni domanda)

- Prendi la domanda
- La trasformi in vettore con Ollama
- Cerchi i documenti simili nel DB
- Passi i documenti + domanda a Ollama
- Ricevi la risposta

## Flusso per convertire un documento

### Versione corretta e definitiva del tuo flusso

1. Estraggo il testo dal file (non base64)
2. Divido il testo in chunk
3. Uso l’API /v1/embed di Ollama per trasformare ogni chunk in un vettore
4. Salvo vettori + testo nel DB
5. Alla domanda: trasformo la domanda in vettore con Ollama
6. Confronto il vettore della domanda con i vettori dei chunk tramite cosine similarity
7. Recupero i Top-K chunk e li passo a Ollama per la risposta

Questa pipeline è 100% corretta.

> prendo il documento → estraggo il testo → lo divido in chunk → passo i chunk a Ollama

### Come si definisce un chunk “buono”

Regola pratica (industry standard)

<pre>
Dimensione:

200–500 parole

oppure 500–1000 token

Overlapping:

10–20% di sovrapposizione

Unità semantica:

paragrafi, sezioni, sottosezioni

📌 L’overlap serve a non “tagliare” i concetti.
</pre>

### Perché NON devi passare tutto il file a Ollama

Tre motivi critici:

1. Limite di token:Embedding model ≠ LLM da chat. Testi lunghi → embedding pessimo
2. Rumore semantico:Un chunk troppo grande:

- contiene più concetti
- genera un vettore “medio”
  -perde precisione

3. Retrieval inefficiente:Se il chunk è enorme:

- il matching è meno preciso
  -recuperi testo inutile

## Funzione di cosine

- numeratore: somma dei prodotti elemento per elemento (**ai\*bi**)
- denominatore: prodotto delle radici quadrate delle somme degli elementi al quadrato (**sqrt(ai^2)\*sqrt(bi^2)**)

**Python** è il migliore per rappresentare questa funzione

<pre>
cos = dot(a, b) / (norm(a) * norm(b))
</pre>

**Ruolo reale della chat (una sola cosa)**
_La chat serve solo a:trasformare contesto + domanda in linguaggio naturale_

## Flusso

1. Recupero chunk embedding dal DB
2. Embedding della domanda (ollama.embed)
3. Calcolo cosine(query, chunk_i) per ogni chunk
4. Ordino per similarità
5. Seleziono Top-K chunk
6. Passo domanda + Top-K chunk a ollama.chat
7. Ottengo risposta in linguaggio naturale

## Cos’è Top-K?

Top-K significa “i K elementi migliori” secondo un criterio di ordinamento.

Nel contesto della RAG:

hai una lista di chunk

per ciascuno calcoli un punteggio di similarità (cosine similarity)

ordini la lista dal punteggio più alto al più basso

prendi i primi K elementi

📌 K è un numero che scegli tu (es. 3, 5, 10).

**Perché non prendere “tutti quelli > 0.8”?**

Perché:

non esiste una soglia universale (dipende dal modello)

potresti avere:

troppi chunk (rumore)

pochi chunk (mancanza di contesto)

Top-K è semplice e robusto.

**Valori tipici di K**

- K = 3 → contesto corto, veloce
- K = 5 → bilanciato
- K = 10 → più contesto, ma rischio di rumore

# Spiegazione chat ollama

Punti importanti da ricordare:

- Senza user il modello non sa cosa fare (come nel tuo esempio iniziale)
- Senza assistant nelle conversazioni lunghe, il modello perde il contesto
- Il system rimane attivo per tutta la sessione
- Ogni nuova chiamata API deve ri-includere tutta la conversazione (Ollama non mantiene stato tra chiamate)

### Chat con system

1. Definire il ruolo/persona: _sono ..._
2. Impostare il formato delle risposte: _rispondi sempre in italiano ..._
3. Definire limiti e restrizioni: _non rispondere se non sei sicuro ..._

Posso essere utilizzati dei **PATTERN**

1. Persona più regole
<pre>
Sei [RUOLO]. 
Le tue caratteristiche sono: [CARATTERISTICHE].
Le tue regole sono:
1. [REGOLA 1]
1. [REGOLA 2]
1. [REGOLA 3]
</pre>

1. Struttura della risposta
<pre>
Rispondi seguendo questo formato:
1. [PRIMO PUNTO]
1. [SECONDO PUNTO]
1. [TERZO PUNTO]
</pre>

1. Few-shot nel system prompt: Puoi includere esempi direttamente nel system

#### Best practices:

- Sii specifico → Meglio "Rispondi in massimo 3 frasi" che "Sii conciso"
- Usa comandi chiari → "Fai X, non fare Y"
- Dai esempi → Mostra cosa vuoi con esempi concreti
- Testa e perfeziona → I system prompt vanno ottimizzati
- Considera la lunghezza → Di solito 50-300 token è ottimale

## Perché devi chiamare la chat alla fine?

**Analogia:**

- DB vettoriale = Una biblioteca che trova libri rilevanti
- LLM = Un studioso esperto che legge quei libri e sintetizza una risposta

**Senza LLM avresti solo:**

- I 3 chunk più simili (testo grezzo)
- Ma non una risposta strutturata alla tua domanda

**Con LLM ottieni:**

1. Sintesi dei chunk rilevanti
2. Risposta diretta alla domanda specifica
3. Formattazione chiara e leggibile
4. Estrazione delle informazioni chiave

<table>
<thead>
<tr>
<th>Componente</th>
<th>Cosa fa</th>
<th>Limiti</th>
</tr>
</thead>
<tbody>
<tr>
<td>DB Vettoriale</td>
<td>Trova documenti simili</td>
<td>Non capisce, non sintetizza</td>
</tr>
<tr>
<td>Cosine Similarity</td>
<td>Misura similarità semantica</td>
<td>Non spiega PERCHÉ sono simili</td>
</tr>
<tr>
<td>Chat LLM</td>
<td>Legge, comprende, sintetizza, risponde</td>
<td>Ha bisogno di buon contest</td>
</tr>
</tbody>
</table>

*La chat non è un "optional" ma il motore di sintesi che trasforma "informazioni simili" in "risposta precisa".*

## Il problema del chunking

**Best Practices dal Mondo Reale**
- Non esiste una soluzione universale - Devi testare diverse strategie
- Usa metadati - Salva info su file, pagina, sezione
- Considera la query - Chunk più piccoli per domande specifiche, più grandi per domande generali
- Testa con domande reali - Il miglior test è: "Questo chunk può rispondere a una domanda?"

**Strumenti di valutazione:**

Se i chunk sono troppo piccoli:

- Perdi il contesto
- La risposta è frammentata
- La similarità diminuisce

Se i chunk sono troppo grandi:

- Perdi precisione
- Aumenta il rumore semantico
- La similarità diminuisce

## LangChain 

LangChain è un framework Python per costruire applicazioni basate su LLM. È diventato lo standard de facto per le RAG perché astrae la complessità.

Pensa a LangChain come al "Laravel" o "Django" degli LLM: invece di scrivere tutto da zero, ti dà componenti pre-costruiti.

> Senza LangChain = Costruire una casa mattone per mattone
> Con LangChain = Usare pareti prefabbricate

### Componenti

**Modelli**:

<pre>
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama

# OpenAI
llm_openai = ChatOpenAI(model="gpt-4")

# Ollama (il tuo caso!)
llm_ollama = Ollama(model="llama3")

# Hugging Face, Anthropic, Google, ecc.
</pre>

**Prompts**:

<pre>
from langchain.prompts import ChatPromptTemplate

template = """
Sei un esperto di {argomento}.
Contesto: {contesto}
Domanda: {domanda}
Rispondi in italiano.
"""

prompt = ChatPromptTemplate.from_template(template)

# Riutilizzi lo stesso template con dati diversi
formatted_prompt = prompt.format(
    argomento="informatica",
    contesto="I computer sono macchine...",
    domanda="Cos'è un computer?"
)
</pre>

**Chains**:

Collegano componenti in flussi:

<pre>
from langchain.chains import LLMChain

chain = LLMChain(llm=llm_ollama, prompt=prompt)

# Esegui tutto in una volta
result = chain.run(
    argomento="storia",
    contesto="La seconda guerra mondiale...",
    domanda="Quando è finita?"
)
</pre>

**Memory**:
Mantiene la memoria delle conversazioni passate
<pre>
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
memory.save_context(
    {"input": "Ciao, mi chiamo Marco"},
    {"output": "Ciao Marco! Come posso aiutarti?"}
)

# La prossima volta ricorderà
print(memory.load_memory_variables({}))
# Output: {'history': 'Human: Ciao, mi chiamo Marco\nAI: Ciao Marco! Come posso aiutarti?'}
</pre>

**Indici**:

<pre>
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Carica documenti
from langchain_community.document_loaders import TextLoader
loader = TextLoader("documento.txt")
documents = loader.load()

# 2. Chunking (il problema che hai tu!)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(documents)

# 3. Embedding
embeddings = OllamaEmbeddings(model="llama3")

# 4. Database vettoriale
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings
)
</pre>

**Agenti**:

<pre>
from langchain.agents import create_react_agent
from langchain.tools import Tool

# Definisci tool personalizzati
calculator_tool = Tool(
    name="Calculator",
    func=lambda x: eval(x),
    description="Calcola espressioni matematiche"
)

# L'LLM decide quando usare il tool
agent = create_react_agent(llm=llm_ollama, tools=[calculator_tool])
</pre>

## Alternative a LangChain


#### LlamaIndex - Ottimizzato per RAG
<pre>
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Più semplice per RAG basiche
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("La tua domanda")
</pre>

## Passaggi nel codice con LangChain

<pre>
# 1. RECURSIVE CHARACTER TEXT SPLITTER
#   ↓
# Fa il CHUNKING intelligente
#   ↓
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500)
chunks = text_splitter.split_documents(documents)
# ✅ CORRETTO!

# 2. CHROMA.FROM_DOCUMENTS
#   ↓
# Crea EMBEDDING (vettori) + Salva in DB
#   ↓
vectorstore = Chroma.from_documents(chunks, OllamaEmbeddings(model="llama3"))
# ✅ CORRETTO! 
# Internamente chiama Ollama per ogni chunk e salva i vettori

# 3. RETRIEVALQA.FROM_CHAIN_TYPE
#   ↓
# Istanzia la "CHAT" con contesto automatico
#   ↓
qa_chain = RetrievalQA.from_chain_type(
    llm=Ollama(model="llama3"),          # Il modello LLM
    retriever=vectorstore.as_retriever() # Il retriever (DB vettoriale)
)
# ✅ CORRETTO!
# Crea una pipeline che: query → retrieve → prompt → risposta

# 4. QA_CHAIN.RUN("DOMANDA")
#   ↓
# Fa il RUN completo della pipeline RAG
#   ↓
risposta = qa_chain.run("Come estrarre il contenuto semantico?")
# ✅ CORRETTO!
# Esegue: embedding query → ricerca similarità → costruzione prompt → chiamata LLM

# QUESTA è la magia che LangChain fa per te:
def cosa_succede_dietro_le_quinte(domanda):
    # 1. Converti la domanda in embedding
    query_embedding = OllamaEmbeddings(model="llama3").embed_query(domanda)
    
    # 2. Cerca nel DB vettoriale i chunk più simili
    chunk_similari = vectorstore.similarity_search_by_vector(query_embedding, k=3)
    
    # 3. Costruisce il prompt AUTOMATICAMENTE
    context = "\n\n".join([chunk.page_content for chunk in chunk_similari])
    prompt = f"""
    Contesto:
    {context}
    
    Domanda: {domanda}
    
    Rispondi basandoti solo sul contesto sopra.
    """
    
    # 4. Chiama l'LLM
    risposta = Ollama(model="llama3").invoke(prompt)
    
    return risposta
</pre>