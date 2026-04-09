import os 
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from chunks.select_chunk import SelectChunk
from datetime import datetime
try:
    print(f"start: {datetime.now()}")
    print("-"*60)
    print("test_chunks_sql")
    print("-"*60)
    SelectChunk(4)
except Exception as e:
    raise e
