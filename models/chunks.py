import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.models import Models

class Chunks(Models):
    def __init__(self):
        super().__init__()
        self.table = "CHUNKS"
        self.columns = ["id", "document_id","content","order_chunk","strategy_chunk_id","token_count","overlap_token","metadata","is_convert_embeded"]
        self.join = [{"table": "DOCUMENTS", "table_id": "document_id"}, {"table": "STRATEGY_CHUNKS", "table_id": "strategy_chunk_id"}]
