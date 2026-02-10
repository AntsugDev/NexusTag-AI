import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from langchain_ollama import OllamaEmbeddings
import asyncio 
from database.model.jobs_failed import JobsFailed
class Embed:
    def __init__(self, chunk,document_id,row_id,strategy_chunk,token_count,overlap_token):
        self.chunck_pre = chunk
        self.ollama = OllamaEmbeddings(model=OLLAMA_MODEL)
        self.max_try = 3
        self.jobs_failed = JobsFailed()
        self.document_id = document_id
        self.row_id = row_id
        self.strategy_chunk = strategy_chunk
        self.token_count = token_count
        self.overlap_token = overlap_token

    async def embed(self):
        try:
            for i,text in enumerate(self.chunck_pre):
                task = asyncio.create_task(self.ollama.aembed_query(text))
                try_i = 0
                while try_i < self.max_try:
                    try:
                        result = await task
                        if len(result):
                            break
                    except Exception as e:
                        try_i += 1
                        if try_i == self.max_try:
                            #jobs failed
                            self.jobs_failed.insert_job_failed({
                                "document_id": self.document_id,
                                "row_id": i,
                                "meta_data": {
                                    "content": self.chunck_pre[i],
                                    "order_chunk": i,
                                    "strategy_chunk": self.strategy_chunk,
                                    "token_count": self.token_count,
                                    "overlap_token": self.overlap_token
                                },
                                "exception": str(e)
                            })
                            continue
        except Exception as e:
            raise e    
        