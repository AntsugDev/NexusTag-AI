import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.models import Model

class Embeddings(Model):
    def __init__(self):
        super().__init__()
        self.table = "EMBEDDINGS"
        self.columns = ["id", "chunk_id","question_id","embedding"]
