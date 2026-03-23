import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.documents import Documents
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from models.chunks import Chunks
from models.strategy_chunk import StrategyChunk
load_dotenv()
import tiktoken

class GeneralChunk(ABC):
    def __init__(self,document:dict,token:int):
        self.document = document
        self.content = None
        if self.document:
           with open(os.path.join(os.getcwd(), 'import-data',self.document.get('name_file')), 'r',encoding='utf-8') as f:
               self.content = f.read()
        else:
            raise ValueError(f"Document not found: {document_id}")
        self.token = os.getenv("MIN_TOKEN",token)    
        self.overlap = float(self.token) * 0.1 
        self.chunks = Chunks()
        self.strategy_chunks = StrategyChunk()

    def get_strategy_chunk(self, strategy:str):
        response = self.strategy_chunks.findBy({
            "label": strategy
        })    
        if response:
            return response[0].get('id')
        else:
            raise ValueError(f"Strategy chunk not found: {strategy}")
    
    def count_token(self,text:str):
        encoding = None
        try:
            encoding = tiktoken.get_encoding("cl100k_base")
        except Exception as e:
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        if encoding:
            return len(encoding.encode(text))
        else:
            raise ValueError("Error counting token")   

    @abstractmethod
    def chunk(self):
        pass
        