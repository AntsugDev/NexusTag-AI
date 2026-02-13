import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.model.model_general import ModelGeneral

class JobsFailed(ModelGeneral):
    def __init__(self):
        self.table = "jobs_failed"

    def insert_job_failed(self, data):
        meta_data = data.get("meta_data")
        if isinstance(meta_data, dict):
            meta_data = json.dumps(meta_data)
            
        return self.insert({
            "document_id": data.get("document_id"),
            "row_id": data.get("row_id"),
            "meta_data": meta_data,
            "exception": data.get("exception")
        })

    def get_last_error(self, document_id):
        # Fetch the most recent error for this document
        s = f"SELECT exception FROM {self.table} WHERE document_id = ? ORDER BY created_at DESC LIMIT 1"
        result = self.execute(s, (document_id,), one=True, fetch=True)
        return result["exception"] if result else "No error details available"