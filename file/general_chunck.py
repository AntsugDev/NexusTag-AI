from abc import ABC, abstractmethod
import os
from langchain_ollama  import OllamaEmbeddings
from embed.embed_service import Embed
from database.model.chunks_table import ChunkTable
from database.model.jobs_failed import JobsFailed
from dotenv import load_dotenv
from ollama import OllamaEmbeddings
from database.model.emebed_model import EmbedModel

load_dotenv()



class GeneralChunck(ABC):
    def __init__(self, file, type_file, document_id):
        if not os.path.exists(file):
            raise Exception("File not found")
        self.file = file   
        self.document_id = document_id
        self.type_file = type_file
        
        # Caricamento variabili da .env
        self.k_overlap = int(os.getenv("K_OVERLAP", 10))
        self.k_max_token = int(os.getenv("K_MAX_TOKEN", 700))
        self.k_min_token = int(os.getenv("K_MIN_TOKEN", 300))
        
        self.standard_token = 500
        self.standard_overlap = int(self.standard_token / (self.k_overlap / 100)) 
        
        self.chunck_size_min = int(os.getenv("K_BINARY_MIN_CHUNK", 3))
        self.chunck_size_max = int(os.getenv("K_BINARY_MAX_CHUNK", 5))
        
        self.task_resolved = 0
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
        self.ollama = OllamaEmbeddings(
             model=self.ollama_model,
        )

    def setToken(self, token:int): 
        if token > self.k_max_token or token < self.k_min_token:
            raise Exception(f"The value token must be between {self.k_min_token} and {self.k_max_token}")
        self.standard_token = token

    def setOverlap(self, overlap:int):
        if token > K_MAX_OVERLAP or token < K_MIN_OVERLAP:
            raise Exception("The value overlap is between 10 and 20")
        self.standard_overlap = overlap    

    @abstractmethod
    def chunck(self) -> list[dict]:
        """
        Deve restituire una lista di chunk strutturati:
        [
            {
                "content": "Testo estratto...",
                "metadata": {"row": 1, "sheet": "Sheet1", "total_pages": 1}
            },
            ...
        ]
        """
        pass

    async def embed(self):
       try:
        chunck_pre = self.chunck()
        if chunck_pre :
            await Embed(chunck_pre,self.document_id,self.row_id,self.strategy_chunk,self.token_count,self.overlap_token).embed()
        else:
            raise Exception("Cannot create embeded because chuck is null or is not reading.")    

       except Exception as e:
        raise e 
    
    def strategy_chunk(self):
        match self.type_file:
            case "txt" |"log"|"md"|"sql":
                return STRATEGY_CHUNK_TESTUALE
            case "csv"|"xls"|"xlsx":
                return STRATEGY_CHUNK_ROW
            case "pdf"|"doc"|"docx"|"docs":
                return STRATEGY_CHUNK_DOC
            case _:
                return STRATEGY_CHUNK_GENERICO   