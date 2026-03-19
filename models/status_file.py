import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.models import Model

class StatusFile(Model):
    def __init__(self):
        super().__init__()
        self.table = "STATUS_FILES"
        self.columns = ["id", "label"]
