import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .model_general import ModelGeneral
class EmbedModel(ModelGeneral):
    def __init__(self):
        self.table = "embeddings"

    def insert_embed(self,data):
        return self.insert({
            "chunk_id": data.chunk_id,
            "embedding": data.embedding,
            "model": data.model,
            "dimension": data.dimension
        })