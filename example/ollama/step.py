import numpy as np
import ollama

# -----------------------------
# 1) Documenti (simulazione DB)
# -----------------------------
documents = [
    "Ollama è un server locale che permette di eseguire Large Language Model.",
    "La RAG è un sistema che combina retrieval + LLM per rispondere usando documenti.",
    "Gli embedding trasformano testo in vettori numerici per confronti di similarità."
]

# -----------------------------
# 2) Funzione embedding
# -----------------------------
def get_embedding(text: str):
    emb = ollama.embed(model="llama3", input=text)
    return np.array(emb.embeddings)   # <- estrai embedding

# -----------------------------
# 3) Ingestione documenti
# -----------------------------
db_vectors = [get_embedding(doc) for doc in documents]

# -----------------------------
# 4) Funzione similarità cosine
# -----------------------------
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# -----------------------------
# 5) Query
# -----------------------------
query = "Cos’è la RAG e come funziona?"
query_vec = get_embedding(query)

# Trova il documento più simile
scores = [cosine_similarity(query_vec, v) for v in db_vectors]
best_index = int(np.argmax(scores))
best_doc = documents[best_index]

print("Documento più simile trovato:")
print(best_doc)
print("Score:", scores[best_index])

# -----------------------------
# 6) Prompt con contesto
# -----------------------------
prompt = f"""
Usa SOLO questo documento per rispondere:

{best_doc}

Domanda:
{query}
"""

# -----------------------------
# 7) Chiamata a Ollama (LLM)
# -----------------------------
response = ollama.chat(
    model="llama3",
    messages=[{"role": "user", "content": prompt}]
)

print("\nRisposta del modello:")
print(response["message"]["content"])
