import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.models import Model

class Documents(Model):
    def __init__(self):
        super().__init__()
        self.table = "DOCUMENTS"
        self.columns = ["id", "user_id", "name_file", "size", "mime_type", "tags_id", "status_id"]
        self.join = [{"table": "USERS", "table_id": "user_id"}, {"table": "TAGS", "table_id": "tags_id"}, {"table": "STATUS_FILES", "table_id": "status_id"}]
