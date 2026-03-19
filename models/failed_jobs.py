import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.models import Model

class FailedJobs(Model):
    def __init__(self):
        super().__init__()
        self.table = "FAILED_JOBS"
        self.columns = ["id", "job_id","exception"]
        self.join = [{"table": "JOBS", "table_id": "job_id"}]
