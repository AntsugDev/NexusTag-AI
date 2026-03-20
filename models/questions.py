import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.models import Models

class Questions(Models):
    def __init__(self):
        super().__init__()
        self.table = "QUESTIONS"
        self.columns = ["id", "tags_id","content"]
        self.join = [{"table": "TAGS", "table_id": "tags_id"}]
