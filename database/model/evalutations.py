import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .model_general import ModelGeneral 

class Evaluations(ModelGeneral):
    def __init__(self):
         self.table = "evaluations"

    def insert_evaluation(self, document_id, avg_score, total_score, random_chunks_evaluation, metadata):
        return self.insert({
            "document_id": document_id,
            "avg_score": avg_score,
            "total_score": total_score,
            "random_chunks_evaluation": random_chunks_evaluation,
            "metadata": metadata
        })

    def get_evaluation(self, document_id):
        return self.get_by_field("document_id", document_id)

    def get_all_evaluations(self):
        return self.get_all()