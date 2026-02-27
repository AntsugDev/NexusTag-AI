import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .model_general import ModelGeneral 
from database.model.documents import Documents
class Evaluations(ModelGeneral):
    def __init__(self):
         self.table = "evaluations"

    def calculate_score(self, total_evalutation, avg, mime_type_file):
        if mime_type_file == "csv" or mime_type_file == "excel":
            return total_evalutation
        elif mime_type_file == "world" or mime_type_file == "pdf":
            return (total_evalutation*0.3) + (avg*0.7)
        else :
            return (total_evalutation*0.4)+(avg*0.6)

    def documentById(self,id):
        try:
           data = Documents().select_document(id)
           if data:
                return data
           else: return None    
        except:
            return None

    def get_topic(self, data = None):
        try:
            if data:
               topic = data.get("topic")
               return topic
            else: return None    
        except:
            return None
    
    def get_strategy_chunk(self, data = None):
        try:
           if data:
             from database.model.chunks_table import ChunkTable
             chunk_table = ChunkTable()
             chunks = chunk_table.get_chunks_by_document_id(data.get("id"),columns=['distinct strategy_chunk'])
             if chunks:
                 return dict(chunks[0]).get("strategy_chunk")
             else: 
                return None    
           else: return None    
        except:
            return None

    def _mime_type(self, data= None):
        try:
           if data:
               return data.get("mime_type")
           else: return None    
        except:
            return None    

    def insert_evaluation(self, evaluations_request):
        data = self.documentById(evaluations_request.document_id)
        topic = self.get_topic(data)
        strategy_chunk = self.get_strategy_chunk(data)
        mime_type = self._mime_type(data)
        if not topic or not strategy_chunk:
            raise Exception("Topic or strategy chunk not found")
        score = self.calculate_score(evaluations_request.total_evaluation, evaluations_request.avg_tokens, mime_type)
        if not score:
            raise Exception("Score not calculated")
        convert = [dict(evalutation) for evalutation in evaluations_request.evalutation_for_row ]
        return self.insert({
            "document_id": evaluations_request.document_id,
            "strategy_chunk": strategy_chunk,
            "topic": topic,
            "mime_type_file": mime_type,
            "total_chunks": evaluations_request.total_chunks,
            "avg_tokens": evaluations_request.avg_tokens,
            "total_token": evaluations_request.total_token,
            "evalutation_for_row": str(convert),
            "total_evaluation": evaluations_request.total_evaluation,
            "score": score
        })

    def get_evaluation(self, document_id):
        return self.search(data={"document_id": document_id})

    def get_all_evaluations(self,page=1, limit=5, join_table=None, columns=None):
        return self.paginate(page=page, limit=limit, join_table=join_table, columns=columns)