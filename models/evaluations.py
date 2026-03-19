import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.models import Model

class Evaluations(Model):
    def __init__(self):
        super().__init__()
        self.table = "EVALUATIONS"
        self.columns = ["id", "document_id","strategy_chunk","tags_id","mime_type_file","total_chunks","avg_tokens","total_token","evalutation_for_row","total_evaluation","score"]
        self.join = [{"table": "DOCUMENTS", "table_id": "document_id"}, {"table": "STRATEGY_CHUNKS", "table_id": "strategy_chunk"}, {"table": "TAGS", "table_id": "tags_id"}]
