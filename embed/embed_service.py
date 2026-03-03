import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from langchain_ollama import OllamaEmbeddings
import asyncio 
import json
from database.model.jobs_failed import JobsFailed
from database.model.emebed_model import EmbedModel
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

    async def embed(self):
        try:
            try_i = 0
            while try_i < self.max_try:
                try:
                    # Eseguiamo l'embedding
                    result = await self.ollama.aembed_query(self.content)
                    if result and len(result) > 0:
                        self.embed_model.insert_embed({
                            "chunk_id": self.chunk_id,
                            "embedding": result,
                        })
                        break
                except Exception as e:
                    try_i += 1
                    if try_i == self.max_try:
                        self.jobs_failed.insert_job_failed({
                            "document_id": self.document_id,
                            "row_id": self.chunk_id,
                            "meta_data": json.dumps({
                                "content": self.content,
                                }),
                                "exception": str(e)
                            })
        except Exception as e:
            print(f"Errore critico in Embed service: {e}")
            raise e
        