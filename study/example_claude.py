from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import SQLiteVec
from langchain_ollama import OllamaEmbeddings
import os
import sys
from datetime import datetime

try:
    start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"start: {start}")
    path = os.path.join('import-data','document.txt')
    print(f"file path:{path}")
    if(not os.path.exists(path)):
        print(f"file not exists:{path}")
        sys.exit(1)
    # 1. Carica
    loader = TextLoader(path, encoding="utf-8")
    documents = loader.load()
    
    #from langchain_community.document_loaders import UnstructuredFileLoader
    # Non importa se è un .pdf, .docx, .txt o .html
    #loader = UnstructuredFileLoader("./documento_misterioso.pdf")
    # Carica il file e lo trasforma in una lista di Documenti LangChain
    #docs = loader.load()

    # 2. Dividi
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    print(f"Chunk creati: {len(chunks)}")

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # 4. Indicizza su SQLiteVec
    vectorstore = SQLiteVec.from_documents(
        documents=chunks,
        embedding=embeddings,
        db_file="knowledge_base.db",
        table="testo"
    )

    print("Indicizzazione completata!")

    # 4. Cerca
    # vectorstore.similarity_search("agenda", k=3)
    end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"end: {end}")

except Exception as e:
    print(e)
