import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.models import Model

class Jobs(Model):
    def __init__(self):
        super().__init__()
        self.table = "JOBS"
        self.columns = ["id", "uuid","metadata"]
