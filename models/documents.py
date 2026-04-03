import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.models import Models

class Documents(Models):
    def __init__(self):
        super().__init__()
        self.table = "DOCUMENTS"
        self.columns = ["DOCUMENTS.id as document_id", "name_file", "size", "mime_type","USERS.id as user_id","USERS.username as username",'TAGS.label as tag','TAGS.id as tag_id','STATUS_FILES.label as status','STATUS_FILES.id as status_id']
        self.join = [{"table": "USERS", "table_id": "user_id"}, {"table": "TAGS", "table_id": "tags_id"}, {"table": "STATUS_FILES", "table_id": "status_id"}]

    def insert_custom(self, data:dict):
        try:
           from models.tags import Tags
           t = Tags()
           find = t.findBy([{"column": "label", "operator": "=", "value": data["argument"], "type": "AND"}])
           if find:
              data["tags_id"] = find[0]["id"]
           else:
              data["tags_id"] = t.insert({"label": data["argument"]})
           from models.status_file import StatusFile
           s = StatusFile()
           find = s.findBy([{"column": "label", "operator": "=", "value": "uploaded", "type": "AND"}])
           if find:
              data["status_id"] = find[0]["id"]
           else:
              raise Exception("Status file 'uploaded' not found")

           return self.insert({
            "user_id":data["user_id"],
            "name_file":data["name_file"],
            "size":data["size"],
            "mime_type":data["mime_type"],
            "tags_id":data["tags_id"],
            "status_id":data["status_id"]
           })

        except Exception as e:
            raise e

    def update_status(self,document_id:int,status_id:str):
        try:
           from models.status_file import StatusFile
           s = StatusFile()
           find = s.findBy([{"column": "label", "operator": "=", "value": status_id, "type": "AND"}])
           if find:
              data = find[0]["id"]
           else:
              raise Exception("Status file not found")
           return self.updateById(document_id,{"status_id":data})
        except Exception as e:
            raise e    
