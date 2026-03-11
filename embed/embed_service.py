import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from langchain_ollama import OllamaEmbeddings
from langchain_community.embeddings import FastEmbedEmbeddings
import asyncio 
import json
from database.model.jobs_failed import JobsFailed
from database.model.emebed_model import EmbedModel
import sqlite_vec
class Embed:
    def __init__(self, content:[], document_id:int, chunk_id:[] = [], query_id:[] = []):
        self.content = content
        self.chunk_id = chunk_id
        self.query_id = query_id
        self.document_id = document_id
        # self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
        self.ollama =FastEmbedEmbeddings(
                     model_name="BAAI/bge-m3",
                     threads=8 
                    )
        
        #  OllamaEmbeddings(
        #     model=self.ollama_model,
        #     base_url=os.getenv("OLLAMA_URL", "http://localhost:11434")
        # )
        self.max_try = 3
        self.jobs_failed = JobsFailed()
        self.embed_model = EmbedModel()

    def embed(self):
        try:
            vettori = self.ollama.embed_documents(self.content)
            if vettori:
                if len(self.chunk_id) > 0:
                   for chunk_id, vettore in zip(self.chunk_id, vettori): 
                        serialized_embedding = sqlite_vec.serialize_float32(vettore)
                        self.embed_model.insert_embed({
                                    "chunk_id": chunk_id,
                                    "query_id" :None,
                                    "embedding": serialized_embedding,
                         })
                elif len(self.query_id) > 0:
                    for query_id, vettore in zip(self.query_id, vettori): 
                        serialized_embedding = sqlite_vec.serialize_float32(vettore)
                        self.embed_model.insert_embed({
                                    "chunk_id": None,
                                    "query_id" :query_id,
                                    "embedding": serialized_embedding,
                         })         
            else: raise Exception(f"Emebeding for document id {self.document_id} not created")
        except Exception as e:
            self.jobs_failed.insert({
                                "document_id": self.document_id,
                                "meta_data": json.dumps({
                                    "content": self.content,
                                    "chunk_id":self.chunk_id,
                                    "query_id":self.query_id
                                    }),
                                "exception": str(e)
                                })
            return                    
        