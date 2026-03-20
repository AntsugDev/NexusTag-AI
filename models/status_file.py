import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.models import Models

class StatusFile(Models):
    def __init__(self):
        super().__init__()
        self.table = "STATUS_FILES"
        self.columns = ["id", "label"]
