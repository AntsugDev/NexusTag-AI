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
from langchain_ollama import OllamaEmbeddings
from datetime import datetime
from langchain_core.documents import Document
from langchain_community.vectorstores import SQLiteVec

class GeneralChunk(ABC):
    def __init__(self,document:dict,loader,tag:str,token:int = None):
        self.document = document
        try:
            self.content = loader[0].page_content
        except Exception as e:
            try:
                self.content = loader.page_content
            except Exception as e:
                self.content = loader
        self.token = os.getenv("MIN_TOKEN",token)  
        self.tag = tag  
        self.overlap = int(float(self.token) * 0.1)
        self.chunks = Chunks()
        self.strategy_chunks = StrategyChunk()
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

    def get_strategy_chunk(self, strategy:str):
        response = self.strategy_chunks.findBy(where=[{"column":"label","operator":"=","value":strategy,"type":"WHERE"}])    
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
    
    def del_embeddings(self):
        from models.embeddings import Embeddings
        e = Embeddings()
        e.statment(f"DELETE FROM embeddings WHERE json_extract(metadata, '$.document_id') = {self.document.get('document_id')}")

    def set_status(self,status:str):
        from models.documents import Documents
        d = Documents()
        return d.update_status(self.document.get('document_id'),status)
    
    def create_embeddings(self,docs):
        try:
            path_database = os.path.join('database','nexus-tag-ai.sqlite')
            if not os.path.exists(path_database):
                raise ValueError("Path database not found")
            vectorstore = SQLiteVec.from_documents(
                documents=docs,
                embedding=self.embeddings,
                db_file=path_database,
                table="embeddings"
            )
            return vectorstore
        except Exception as e:
            raise e   
    def remove_file(self):
        path_file = os.path.join(os.getcwd(), 'import-data',self.document.get('name_file'))
        if os.path.exists(path_file):
            os.remove(path_file)

    def save_chunk(self,chunks:[]):
        self.del_embeddings()
        try:

          
            docs = [
                Document(
                    page_content=c,
                    metadata={"tag": self.tag, "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "content": c, "document_id": self.document.get('document_id')}
                ) for c in chunks
            ]
            vectorstore = self.create_embeddings(docs)
            if vectorstore:
                self.set_status(completed)
                self.remove_file()
                print(f"end: {datetime.now()}")
            else :
                self.set_status("failed")
                raise ValueError("Vectorstore not found")
                  
        except Exception as e:
            self.set_status("failed")
            raise e

    @abstractmethod
    def chunk(self):
        pass
    @abstractmethod
    def set_save_chunk(self,chunks):
        pass
        