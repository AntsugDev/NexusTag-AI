import os 
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from chunks.select_chunk import SelectChunk
try:
    SelectChunk(2)
    print("ok")
except Exception as e:
    raise e
