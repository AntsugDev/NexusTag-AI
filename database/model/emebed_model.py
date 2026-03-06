import os
import sys
import sqlite_vec
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .model_general import ModelGeneral
class EmbedModel(ModelGeneral):
    def __init__(self):
        self.table = "vss_chunks"

    def insert_embed(self,data):
        serialized_embedding = sqlite_vec.serialize_float32(data.get("embedding"))
        return self.insert({
            "chunk_id": data.get("chunk_id"),
            "embedding": serialized_embedding,
        })