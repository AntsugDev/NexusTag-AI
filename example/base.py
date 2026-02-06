"""
RAG SEMPLIFICATO - Tutorial per capire i concetti base
Senza database vettoriali, solo con liste Python!
"""

# ============================================
# INSTALLAZIONE MINIMA
# ============================================
"""
pip install sentence-transformers numpy ollama
"""

# ============================================
# STEP 1: Import essenziali
# ============================================
from sentence_transformers import SentenceTransformer
import numpy as np
import requests
import json

print("="*70)
print("🎓 RAG SEMPLIFICATO - TUTORIAL STEP-BY-STEP")
print("="*70)

# ============================================
# STEP 2: Prepara i documenti (la nostra "knowledge base")
# ============================================
print("\n📚 STEP 1: Preparazione documenti")
print("-"*70)

# Lista semplice di documenti
documents = [
    "La carbonara si fa con guanciale, uova, pecorino e pepe nero",
    "La pizza margherita ha pomodoro, mozzarella e basilico",
    "Il risotto alla milanese contiene zafferano e parmigiano",
    "Il tiramisù è fatto con savoiardi, caffè, mascarpone e cacao",
    "La pasta al pesto usa basilico, pinoli, aglio e parmigiano"
]

print(f"✅ Caricati {len(documents)} documenti:")
for i, doc in enumerate(documents, 1):
    print(f"   {i}. {doc[:50]}...")

# ============================================
# STEP 3: Carica il modello per gli embeddings
# ============================================
print("\n🧠 STEP 2: Caricamento modello embeddings")
print("-"*70)
print("⏳ Caricamento in corso...")

# Modello leggero per convertire testo in numeri (vettori)
model = SentenceTransformer('all-MiniLM-L6-v2')

print("✅ Modello caricato!")
print(f"   Dimensione vettori: 384 numeri per ogni testo")

# ============================================
# STEP 4: Converti documenti in vettori (embeddings)
# ============================================
print("\n🔢 STEP 3: Creazione embeddings dei documenti")
print("-"*70)

# Converte ogni documento in un vettore di 384 numeri
document_embeddings = model.encode(documents)

print(f"✅ Creati {len(document_embeddings)} vettori")
print(f"   Forma array: {document_embeddings.shape}")
print(f"   Esempio primo vettore (primi 5 numeri): {document_embeddings[0][:5]}")

# ============================================
# STEP 5: Funzione per calcolare similarità
# ============================================
print("\n📐 STEP 4: Funzione di similarità")
print("-"*70)

def cosine_similarity(vec1, vec2):
    """
    Calcola quanto due vettori sono simili (da 0 a 1)
    1 = identici, 0 = completamente diversi
    """
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

# Test similarità tra due documenti
sim = cosine_similarity(document_embeddings[0], document_embeddings[1])
print(f"✅ Similarità tra doc 1 e doc 2: {sim:.4f}")
print(f"   (Carbonara vs Pizza - abbastanza diversi!)")

sim2 = cosine_similarity(document_embeddings[0], document_embeddings[0])
print(f"   Similarità tra doc 1 e doc 1: {sim2:.4f}")
print(f"   (Stesso documento - identico!)")

# ============================================
# STEP 6: Funzione di ricerca (retrieval)
# ============================================
print("\n🔍 STEP 5: Funzione di ricerca")
print("-"*70)

def search_documents(query, top_k=2):
    """
    Cerca i documenti più simili alla domanda
    """
    print(f"\n❓ Query: '{query}'")
    
    # 1. Converti la domanda in vettore
    query_embedding = model.encode([query])[0]
    print(f"   ✓ Query convertita in vettore")
    
    # 2. Calcola similarità con tutti i documenti
    similarities = []
    for i, doc_embedding in enumerate(document_embeddings):
        sim = cosine_similarity(query_embedding, doc_embedding)
        similarities.append((i, sim, documents[i]))
    
    print(f"   ✓ Calcolate {len(similarities)} similarità")
    
    # 3. Ordina per similarità (dal più simile)
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # 4. Prendi i top K documenti
    top_results = similarities[:top_k]
    
    print(f"\n   📊 Top {top_k} risultati:")
    for rank, (doc_idx, similarity, doc_text) in enumerate(top_results, 1):
        print(f"      {rank}. [Score: {similarity:.4f}] {doc_text}")
    
    return top_results

# Test ricerca
results = search_documents("ingredienti della carbonara", top_k=2)

# ============================================
# STEP 7: Connessione a Ollama (LLM)
# ============================================
print("\n🤖 STEP 6: Connessione a Ollama")
print("-"*70)

def call_ollama(prompt, model_name="llama3.2"):
    """
    Chiama Ollama per generare una risposta
    """
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Errore: {response.status_code}"
    except Exception as e:
        return f"Errore connessione Ollama: {e}"

print("✅ Funzione Ollama pronta")
print("   (Assicurati che Ollama sia in esecuzione: ollama serve)")

# ============================================
# STEP 8: RAG completo - Metti tutto insieme!
# ============================================
print("\n🎯 STEP 7: RAG Completo")
print("-"*70)

def rag_answer(question, top_k=2):
    """
    RAG = Retrieval + Generation
    1. Cerca documenti rilevanti (Retrieval)
    2. Genera risposta usando quei documenti (Generation)
    """
    print(f"\n{'='*70}")
    print(f"💬 DOMANDA: {question}")
    print('='*70)
    
    # FASE 1: RETRIEVAL - Cerca documenti simili
    print("\n🔍 FASE 1: RETRIEVAL")
    results = search_documents(question, top_k=top_k)
    
    # Estrai solo il testo dei documenti trovati
    context_docs = [doc_text for _, _, doc_text in results]
    context = "\n".join(context_docs)
    
    # FASE 2: GENERATION - Crea il prompt per l'LLM
    print("\n🤖 FASE 2: GENERATION")
    prompt = f"""Sei un esperto di cucina italiana. 
Rispondi alla domanda usando SOLO le informazioni nel contesto fornito.
Se non sai la risposta, dillo chiaramente.

CONTESTO:
{context}

DOMANDA: {question}

RISPOSTA:"""
    
    print("   ✓ Prompt creato")
    print(f"   ✓ Lunghezza contesto: {len(context)} caratteri")
    
    # Chiama l'LLM
    print("   ⏳ Generazione risposta in corso...")
    answer = call_ollama(prompt)
    
    print(f"\n💡 RISPOSTA FINALE:")
    print(f"   {answer}")
    
    return answer

# ============================================
# STEP 9: Test del sistema RAG
# ============================================
print("\n" + "="*70)
print("🧪 TEST DEL SISTEMA RAG")
print("="*70)

# Test 1: Domanda con risposta nei documenti
rag_answer("Quali sono gli ingredienti della carbonara?")

# Test 2: Altra domanda
rag_answer("Come si prepara il tiramisù?")

# Test 3: Domanda senza risposta
rag_answer("Come si fa la pasta alla norma?")

# ============================================
# STEP 10: Statistiche e visualizzazioni
# ============================================
print("\n" + "="*70)
print("📊 STATISTICHE FINALI")
print("="*70)

def show_similarity_matrix():
    """Mostra quanto sono simili i documenti tra loro"""
    print("\n📈 Matrice di similarità tra documenti:")
    print("\n    ", end="")
    for i in range(len(documents)):
        print(f"Doc{i+1} ", end="")
    print()
    
    for i in range(len(documents)):
        print(f"Doc{i+1} ", end="")
        for j in range(len(documents)):
            sim = cosine_similarity(document_embeddings[i], document_embeddings[j])
            print(f"{sim:.2f}  ", end="")
        print()

show_similarity_matrix()

# ============================================
# BONUS: Funzioni utility per esperimenti
# ============================================
print("\n" + "="*70)
print("🔬 FUNZIONI EXTRA PER SPERIMENTARE")
print("="*70)

def add_document(new_doc):
    """Aggiungi un nuovo documento al sistema"""
    global documents, document_embeddings
    
    documents.append(new_doc)
    new_embedding = model.encode([new_doc])[0]
    document_embeddings = np.vstack([document_embeddings, new_embedding])
    
    print(f"✅ Documento aggiunto! Totale: {len(documents)}")

def compare_queries(query1, query2):
    """Confronta due domande diverse"""
    print(f"\n🔬 CONFRONTO TRA QUERY:")
    print(f"   Query 1: {query1}")
    print(f"   Query 2: {query2}")
    
    emb1 = model.encode([query1])[0]
    emb2 = model.encode([query2])[0]
    
    sim = cosine_similarity(emb1, emb2)
    print(f"\n   Similarità: {sim:.4f}")
    
    if sim > 0.8:
        print("   → Domande molto simili!")
    elif sim > 0.5:
        print("   → Domande abbastanza correlate")
    else:
        print("   → Domande diverse")

# Esempio uso funzioni extra
print("\n📝 Esempio: aggiungo un nuovo documento")
add_document("La pasta all'amatriciana usa guanciale, pomodoro e pecorino")

print("\n📝 Esempio: confronto due query")
compare_queries(
    "ingredienti della carbonara",
    "come si fa la carbonara"
)

# ============================================
# SPIEGAZIONE FINALE
# ============================================
print("\n" + "="*70)
print("📖 RIEPILOGO: COME FUNZIONA IL RAG")
print("="*70)
print("""
1. 📚 DOCUMENTI: Hai una lista di informazioni
   └─→ "La carbonara ha guanciale, uova..."

2. 🔢 EMBEDDINGS: Converti tutto in numeri (vettori)
   └─→ [0.12, -0.45, 0.78, ...] (384 numeri)

3. ❓ QUERY: L'utente fa una domanda
   └─→ "Ingredienti della carbonara?"

4. 🔍 SEARCH: Trova documenti simili
   └─→ Calcola distanza tra vettori
   └─→ Prendi i più vicini (top K)

5. 🤖 LLM: Genera risposta usando quei documenti
   └─→ "La carbonara ha guanciale, uova, pecoreo..."

6. ✅ RISULTATO: Risposta accurata e contestualizzata!

VANTAGGI:
✓ L'LLM ha informazioni aggiornate (i tuoi documenti)
✓ Riduce le "allucinazioni" (inventa meno)
✓ Puoi aggiornare i documenti senza ri-addestrare
✓ Tracciabile: sai da dove viene l'info
""")

print("\n" + "="*70)
print("✅ TUTORIAL COMPLETATO!")
print("="*70)
print("\n💡 PROSSIMI PASSI:")
print("   1. Sperimenta con altre domande")
print("   2. Aggiungi più documenti")
print("   3. Prova diversi valori di top_k")
print("   4. Quando sei pronto, passa a PostgreSQL + pgvector!")