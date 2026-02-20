import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from langchain_ollama import OllamaEmbeddings
import asyncio 
import json
from database.model.jobs_failed import JobsFailed
class Embed:
    def __init__(self, chunks, document_id, strategy_chunk, token_count, overlap_token):
        self.chunks = chunks
        self.document_id = document_id
        self.strategy_chunk = strategy_chunk
        self.token_count = token_count
        self.overlap_token = overlap_token
        
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
        self.ollama = OllamaEmbeddings(
            model=self.ollama_model,
            base_url=os.getenv("OLLAMA_URL", "http://localhost:11434")
        )
        self.max_try = 3
        self.jobs_failed = JobsFailed()

    async def embed(self):
        try:
            for i, chunk in enumerate(self.chunks):
                # Se chunk è un dizionario (riga DB), estraiamo il contenuto
                text = chunk.get("content") if isinstance(chunk, dict) else str(chunk)
                
                if not text:
                    continue

                try_i = 0
                while try_i < self.max_try:
                    try:
                        # Eseguiamo l'embedding
                        result = await self.ollama.aembed_query(text)
                        
                        if result and len(result) > 0:
                            # Qui andrebbe l'inserimento nel DB dei vettori (vss_chunks)
                            # Per ora lo script si ferma alla generazione
                            break
                    except Exception as e:
                        try_i += 1
                        print(f"Tentativo {try_i} fallito per chunk {i}: {e}")
                        if try_i == self.max_try:
                            # Inserimento nei jobs falliti
                            self.jobs_failed.insert_job_failed({
                                "document_id": self.document_id,
                                "row_id": i,
                                "meta_data": json.dumps({
                                    "content": text[:200], # Limitiamo per evitare metadati troppo grandi
                                    "order_chunk": chunk.get("order_chunk", i) if isinstance(chunk, dict) else i,
                                    "strategy_chunk": self.strategy_chunk,
                                    "token_count": self.token_count,
                                    "overlap_token": self.overlap_token
                                }),
                                "exception": str(e)
                            })
        except Exception as e:
            print(f"Errore critico in Embed service: {e}")
            raise e
        