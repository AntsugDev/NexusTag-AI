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
            "size": data.get("size")
        })