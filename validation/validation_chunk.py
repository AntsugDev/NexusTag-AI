import os
import sys
import random
import statistics
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from dotenv import load_dotenv
load_dotenv()

def validate_document_chunks(document_id: int):
    try:
        from database.model.chunks_table import ChunkTable
        db = ChunkTable()
        all_chunks = db.get_chunks_by_document_id(document_id)
        
        if not all_chunks:
            print(f"Nessun chunk trovato per il documento {document_id}")
            return

        # Trasformiamo in lista di dizionari per comodità
        all_chunks = [dict(row) for row in all_chunks]
        total_count = len(all_chunks)
        
        # 1. Calcolo statistiche globali su tutti i chunk del documento
        token_counts = [c.get('token_count', 0) for c in all_chunks]
        
        # Gestione media e deviazione
        avg_tokens = statistics.mean(token_counts) if token_counts else 0
        stdev_tokens = statistics.stdev(token_counts) if len(token_counts) > 1 else 0
        
        print(f"\n" + "="*50)
        print(f"--- Statistiche Documento {document_id} ---")
        print(f"Totale Chunk: {total_count}")
        print(f"Media Token: {avg_tokens:.2f}")
        print(f"Deviazione Standard: {stdev_tokens:.2f}")
        print("="*50 + "\n")

        # 2. Selezione Campioni (Soglie variabili)
        min_threshold = int(os.getenv('K_MIN_RANDOM_CHUNK', 10))
        max_threshold = int(os.getenv('K_MAX_RANDOM_CHUNK', 50))
        
        sampled_chunks = []
        if total_count <= min_threshold:
            sampled_chunks = all_chunks
        else:
            first = all_chunks[0]
            last = all_chunks[-1]
            middle_chunks = all_chunks[1:-1]
            
            # Quanti random estrarre?
            n_random = int(os.getenv('K_MIN_RANDOM_CHUNK', 10)) if total_count > max_threshold else 5
            
            # Assicuriamoci di non chiedere più di quanto disponibile nel mezzo
            actual_sample_size = min(n_random, len(middle_chunks))
            random_samples = random.sample(middle_chunks, actual_sample_size)
            
            # Ordiniamo per mantenere la sequenza logica del documento
            sampled_chunks = [first] + sorted(random_samples, key=lambda x: x['order_chunk']) + [last]

        # 3. Output Validazione
        print(f"--- Analisi Campioni ({len(sampled_chunks)}) ---")
        for c in sampled_chunks:
            tokens = c.get('token_count', 0)
            diff = tokens - avg_tokens
            # Colore/alert visivo manuale se la differenza è alta
            status = "OK"
            if stdev_tokens > 0:
                z_score = diff / stdev_tokens
                if abs(z_score) > 2: status = "ATTENZIONE (Anomalo)"
            
            print(f"ID: {c['id']} | Ordine: {c['order_chunk']} | Token: {tokens} (Diff: {diff:+.1f}) | Status: {status}")
            # Pulizia testo per visualizzazione
            clean_content = c['content'][:150].replace('\n', ' ').strip()
            print(f"Contenuto: {clean_content}...")
            print("-" * 50)

    except Exception as e:
        print(f"Errore durante la validazione: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Eseguiamo il test sul documento ID 1
    validate_document_chunks(1)