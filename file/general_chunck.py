import tiktoken
from abc import ABC, abstractmethod
import os
from langchain_ollama import OllamaEmbeddings
from embed.embed_service import Embed
from database.model.chunks_table import ChunkTable
from database.model.jobs_failed import JobsFailed
from dotenv import load_dotenv
from database.model.emebed_model import EmbedModel
from database.model.strategy import StrategyChunk

load_dotenv()

class GeneralChunck(ABC):
    def __init__(self, file, type_file, document_id = None):
        if not os.path.exists(file):
            raise Exception("File not found")
        self.file = file   
        self.document_id = document_id
        self.type_file = type_file
        
        # Caricamento variabili da .env
        self.k_overlap = int(os.getenv("K_MIN_OVERLAP", 10))
        self.k_max_token = int(os.getenv("K_MAX_TOKEN", 700))
        self.k_min_token = int(os.getenv("K_MIN_TOKEN", 300))
        
        self.standard_token = 500
        self.standard_overlap = int(self.standard_token / self.k_overlap) 
        
        self.chunck_size_min = int(os.getenv("K_BINARY_MIN_CHUNK", 3))
        self.chunck_size_max = int(os.getenv("K_BINARY_MAX_CHUNK", 5))
        
        self.task_resolved = 0
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
        self.ollama = OllamaEmbeddings(
             model=self.ollama_model,
        )
        
        # Inizializzazione tokenizer
        try:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        except Exception:
            self.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")

    def count_tokens(self, text: str) -> int :
        """Calcola il numero reale di token di una stringa."""
        if not text:
            return 0
        return len(self.tokenizer.encode(text))

    def setToken(self, token:int): 
        if token > self.k_max_token or token < self.k_min_token:
            raise Exception(f"The value token must be between {self.k_min_token} and {self.k_max_token}")
        self.standard_token = token

    def setOverlap(self, overlap:int):
        if overlap > int(os.getenv("K_MAX_OVERLAP", 20)) or overlap < int(os.getenv("K_MIN_OVERLAP", 10)):
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

    def embed(self, content,document_id,chunk_id):
       try:
        Embed(
            content=content,
            chunk_id=chunk_id,
            document_id=document_id,
        ).embed()
       except Exception as e:
        raise e 
    
    def strategy_chunk(self):
        s = StrategyChunk()
        match self.type_file:
            case "txt" |"log"|"sql":
                return s.get_by_name(str(os.getenv("STRATEGY_CHUNK_TESTUALE")).strip() )
            case "md":
                return s.get_by_name(str(os.getenv("STRATEGY_CHUNK_MD")).strip())
            case "csv"|"xls"|"xlsx":
                return s.get_by_name(str(os.getenv("STRATEGY_CHUNK_ROW")).strip())
            case "pdf"|"doc"|"docx"|"docs":
                return s.get_by_name(str(os.getenv("STRATEGY_CHUNK_DOC")).strip())
            case _:
                return s.get_by_name(str(os.getenv("STRATEGY_CHUNK_GENERICO")).strip())   
       