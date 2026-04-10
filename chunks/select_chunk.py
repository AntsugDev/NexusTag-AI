import os 
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from chunks.recursive import Recursive
from chunks.recursive_sql import RecursiveSql
from chunks.markdown import Markdown
from models.documents import Documents
from langchain_unstructured import UnstructuredLoader
from langchain_community.document_loaders import TextLoader
from models.tags import Tags

class SelectChunk:
    def __init__(self,document_id:int):
        self.document = Documents().find(document_id)
        if not self.document:
            raise ValueError(f"Document not found: {document_id}")
        self.document =self.document[0]
        path = os.path.join(os.getcwd(), 'import-data',self.document.get('name_file'))
        if not os.path.exists(path):
            raise ValueError(f"File not found: {path}")
        nome_base, estensione = os.path.splitext(self.document.get('name_file'))
        if estensione == '.md':
            loader = TextLoader(path, encoding="utf-8")
        else:     
            loader = UnstructuredLoader(file_path=path)
        docs = loader.load()
        
        mime_type = self.document.get('mime_type')
        tag = Tags().find(self.document.get('tag_id'))
        if not tag:
            raise ValueError(f"Tag not found: {self.document.get('tag_id')}")
        tag = tag[0].get('label')
       
        match self.document.get('mime_type'):
            case "text/plain" | "application/octet-stream" | "application/sql":
                
                if estensione == ".sql":
                    RecursiveSql(self.document,docs,tag).chunk()
                elif estensione == '.md':  
                    Markdown(self.document,docs,tag).chunk()  
                else:
                    Recursive(self.document,docs,tag).chunk()
            case _:    
                raise ValueError(f"Unsupported mime type: {mime_type}")
            # case "application/pdf":
            # case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                
            # case "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
               
            # case "application/vnd.openxmlformats-officedocument.presentationml.presentation":
                
            #     raise ValueError(f"Unsupported mime type: {mime_type}")
    
    