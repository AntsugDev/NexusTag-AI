import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.model.model_general import ModelGeneral

class JobsFailed(ModelGeneral):
    def __init__(self):
        self.table = "jobs_failed"

    def insert_job_failed(self,data):
        return self.insert({
            "document_id": data.id,
            "row_id": data.row_id,
            "meta_data": data.meta_data,
            "exception": data.exception
        })