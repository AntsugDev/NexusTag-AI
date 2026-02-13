import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .model_general import ModelGeneral 

class Documents(ModelGeneral):
    def __init__(self):
         self.table = "documents"

    def insert_file(self, data):
        return self.insert({
            "user_id": data.get("user_id"),
            "name_file": data.get("name_file"),
            "status_file": data.get("status_file", "uploaded"),
            "mime_type": data.get("mime_type"),
            "size": data.get("size"),
            "topic": data.get("topic")
        })

    def get_documents_ready_to_process(self):
        query = f"SELECT * FROM {self.table} WHERE status_file IN ('uploaded', 'error')"
        return self.statment(query, fetch=True)  

    def update_processed(self, id):
        return self.update({"status_file": "processed"}, id) 

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