import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.models import Models

class Chunks(Models):
    def __init__(self):
        super().__init__()
        self.table = "CHUNKS"
        self.columns = ["CHUNKS.id as chunk_id", "CHUNKS.document_id as chunk_document_id","CHUNKS.content as content",
        "CHUNKS.order_chunk as order_chunk","CHUNKS.strategy_chunk_id as strategy_chunk_id","CHUNKS.token_count as token_count","CHUNKS.overlap_token as overlap",
        "CHUNKS.metadata as metadata","CHUNKS.is_convert_embeded as is_convert_embeded",
        "DOCUMENTS.name_file as name_file","DOCUMENTS.size as size","DOCUMENTS.mime_type as mime_type",
        "STRATEGY_CHUNKS.label as strategy_chunk_label"]
        self.join = [{"table": "DOCUMENTS", "table_id": "document_id"}, {"table": "STRATEGY_CHUNKS", "table_id": "strategy_chunk_id"}]
