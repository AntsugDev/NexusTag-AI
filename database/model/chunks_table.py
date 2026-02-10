import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .model_general import ModelGeneral
class ChunkTable(ModelGeneral):
    def __init__(self):
          self.table = "chunks"

    def insert_chunk(self, data):
        print("'Insert chunck' \n .... \n")
        return self.insert({
            "document_id": data.get("id"),
            "content": data.get("content"),
            "order_chunk": data.get("order_chunk"),
            "strategy_chunk": data.get("strategy_chunk"),
            "token_count": data.get("token_count"),
            "overlap_token": data.get("overlap_token"),
            "metadata": data.get("metadata") # Può essere una stringa JSON o dict se gestito dal driver
        })