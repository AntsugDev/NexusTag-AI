import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .model_general import ModelGeneral 
from database.model.topic import TopicChunks
from database.model.strategy import StrategyChunk

class Documents(ModelGeneral):
    def __init__(self):
         self.table = "documents"
         self.topic = TopicChunks()
         self.strategy_chunk = StrategyChunk()

    def insert_file(self, data):
        topic_id = self.topic.get_by_name(data.get("topic"))
        if not topic_id:
            topic_id = self.topic.create(data.get("topic"))

        strategy_chunk_id = self.strategy_chunk.get_by_name(data.get("strategy_chunk"))

        return self.insert({
            "user_id": data.get("user_id"),
            "name_file": data.get("name_file"),
            "status_file": data.get("status_file", "uploaded"),
            "mime_type": data.get("mime_type"),
            "size": data.get("size"),
            "topic": topic_id,
        })

    def get_documents_ready_to_process(self):
        query = f"SELECT * FROM {self.table} WHERE status_file IN ('uploaded', 'error', 'reprocessed')"
        return self.statment(query, fetch=True)  

    def update_processed(self, id):
        return self.update({"status_file": "processed"}, id) 

    def update_reprocessed(self, id):
        return self.update({"status_file": "reprocessed"}, id)     

    def update_pending(self, id):
        return self.update({"status_file": "pending"}, id) 

    def update_error(self, id):
        return self.update({"status_file": "error"}, id)       

    def select_document(self, id):
        show = self.show(id)
        if show:
            return dict(show)
        else:
            raise Exception("Document not found")

    def suggest_topics(self, q):
        query = f"SELECT DISTINCT topic FROM {self.table} WHERE topic LIKE ? LIMIT 5"
        return self.statment(query, (f"%{q}%",), fetch=True)