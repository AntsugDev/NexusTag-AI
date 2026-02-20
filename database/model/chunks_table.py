import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .model_general import ModelGeneral

class ChunkTable(ModelGeneral):
    def __init__(self):
        self.table = "chunks"

    def insert_chunk(self, data):
        return self.insert({
            "document_id": data.get("id"),
            "content": data.get("content"),
            "order_chunk": data.get("order_chunk"),
            "strategy_chunk": data.get("strategy_chunk"),
            "token_count": data.get("token_count"),
            "overlap_token": data.get("overlap_token"),
            "metadata": data.get("metadata")
        })

    def delete_by_document(self, document_id):
        # s_vss = f"DELETE FROM vss_chunks WHERE chunk_id IN (SELECT id FROM {self.table} WHERE document_id = ?)"
        # self.execute(s_vss, (document_id,))
        s = f"DELETE FROM {self.table} WHERE document_id = ?"
        return self.execute(s, (document_id,))

        
    def get_chunks_by_document_id(self, document_id):
        s = self.search({
            "document_id": document_id
        })
        return s

    def is_chunked(self, document_id):
        s = self.count_search({
            "id": document_id
        })
        return self.execute(s, (document_id,))   

      