import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from langchain_ollama import OllamaEmbeddings
import asyncio 
import json
from database.model.jobs_failed import JobsFailed
from database.model.emebed_model import EmbedModel
import sqlite_vec
class Embed:
    def __init__(self, content, chunk_id, document_id):
        self.content = content
        self.chunk_id = chunk_id
        self.document_id = document_id
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
        self.ollama = OllamaEmbeddings(
            model=self.ollama_model,
            base_url=os.getenv("OLLAMA_URL", "http://localhost:11434")
        )
        self.max_try = 3
        self.jobs_failed = JobsFailed()
        self.embed_model = EmbedModel()

    def embed(self, is_return:bool = False):
        try:
            try_i = 0
            while try_i < self.max_try:
                print(f"Tentativo {try_i} di embedding per il chunck {self.chunk_id}")
                try:
                    # Eseguiamo l'embedding
                    result = self.ollama.embed_query(self.content)
                    if result and len(result) > 0:
                        serialized_embedding = sqlite_vec.serialize_float32(data.get("embedding"))
                        if is_return == False and self.chunk_id is not None :
                            print(f"Vector success for chunck {self.chunk_id}")
                            self.embed_model.insert_embed({
                                "chunk_id": self.chunk_id,
                                "embedding": serialized_embedding,
                            })
                            break
                        else : return serialized_embedding
                except Exception as e:
                    try_i += 1
                    if try_i == self.max_try:
                        if is_return == False and self.chunk_id is not None and self.document_id is not None:
                            self.jobs_failed.insert({
                                "document_id": self.document_id,
                                "row_id": self.chunk_id,
                                "meta_data": json.dumps({
                                    "content": self.content,

                                    }),
                                "exception": str(e)
                                })
                        else: raise Exception("Impossible creating the emebedding")       
        except Exception as e:
            print(f"Errore critico in Embed service: {e}")
            raise e
        