Guida: Gestione Documenti per Argomento con LangChain & SQLiteVecQuesta guida illustra come gestire documenti di diversa natura in un unico database vettoriale, utilizzando i metadati per filtrare le ricerche ed evitare "confusioni" tra argomenti diversi.1. Architettura ConcettualeL'idea chiave è non creare tabelle diverse per ogni argomento, ma usare una tabella unica dove ogni frammento di testo (chunk) porta con sé un'"etichetta" (metadata).FaseAzioneRisultatoIngestionCaricamento file + estrazione testoLista di StringheSplittingDivisione in ChunksFrammenti di testoTaggingAggiunta Metadati (es. {"argomento": "fiscale"})Document ObjectsStorageCreazione Embedding e salvataggioDatabase SQLiteVec2. Esempio Pratico di Inserimento (Python)In questa fase, indipendentemente dal tipo di file, forziamo l'argomento nei metadati di ogni chunk.Pythonfrom langchain_community.vectorstores import SQLiteVec
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings # O il tuo modello preferito
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Configurazione
embedding_model = OpenAIEmbeddings()
db_file = "conoscenza_aziendale.db"

def carica_documento(testo_estratto, nome_argomento):
    # 2. Creazione Chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(testo_estratto)
    
    # 3. Creazione Documenti con Metadati applicati a OGNI chunk
    docs = [
        Document(
            page_content=c,
            metadata={"argomento": nome_argomento, "data_caricamento": "2024-05-20"}
        ) for c in chunks
    ]
    
    # 4. Salvataggio su SQLiteVec
    vector_db = SQLiteVec.from_documents(
        docs, 
        embedding_model, 
        db_file=db_file, 
        table_name="documenti_vettoriali"
    )
    return vector_db

# Esempio d'uso:
# carica_documento("Il testo del PDF fiscale...", "fiscale")
# carica_documento("Il testo del manuale tecnico...", "tecnico")
3. Esempio di Ricerca Filtrata (Chat)Quando l'utente interroga il sistema, passiamo il filtro per assicurarci che la ricerca avvenga solo nel "perimetro" dell'argomento scelto.Pythondef chiedi_al_bot(domanda, argomento_scelto):
    # Inizializza il DB esistente
    vector_db = SQLiteVec(
        db_file=db_file,
        table_name="documenti_vettoriali",
        embedding_definition=embedding_model
    )
    
    # Esegue la ricerca filtrata
    # k=4 restituisce i 4 chunk più simili SOLO per quell'argomento
    risultati = vector_db.similarity_search(
        domanda,
        k=4,
        filter={"argomento": argomento_scelto}
    )
    
    return risultati

# Esempio: L'utente ha selezionato "fiscale" nella UI
# risposte = chiedi_al_bot("Quali sono le detrazioni?", "fiscale")
4. Vantaggi di questo approccioFlessibilità del Formato: La logica non cambia se il file è .txt, .pdf o .docx.Efficienza: Il database non deve calcolare la similarità su migliaia di documenti irrilevanti.Semplicità: Hai un solo database da gestire e sottoporre a backup.Scalabilità: Se domani aggiungi un argomento "Risorse Umane", ti basta cambiare la stringa nel filtro senza toccare il codice del database.