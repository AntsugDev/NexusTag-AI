import time
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text",keep_alive=-1)

testo = "testo di prova"

t0 = time.time()
embeddings.embed_query(testo)
print(f"Prima chiamata: {time.time() - t0:.2f}s")  # lenta — carica il modello

t0 = time.time()
embeddings.embed_query(testo)
print(f"Seconda chiamata: {time.time() - t0:.2f}s")  # deve essere < 1s