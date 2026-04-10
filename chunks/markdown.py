import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from chunks.general_chunck import GeneralChunk
from langchain_text_splitters import  MarkdownHeaderTextSplitter, Language
import base64
from langchain_core.documents import Document
from datetime import datetime

class Markdown(GeneralChunk):
    def __init__(self,document:dict,loader,tag:str,token:int = None):
        super().__init__(document,loader,tag,token)
        separator = [
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ]

        self.splitter = MarkdownHeaderTextSplitter(
                headers_to_split_on=separator,
                return_each_line=True
            )

    def split_metadata(self,metadata:dict):
        metadata_list = []
        for k, v in metadata.items():
            if v:
                metadata_list.append(f"{v}")
        return "\t:\t".join(metadata_list)
        
    def chunk(self):
        try: 
            split = self.splitter.split_text(self.content) 
            docs = []
            for s in split:
                metadata = self.split_metadata(s.metadata)
                testo = f"{metadata}\n {s.page_content}"
                docs.append(Document(page_content=testo, metadata={"tag": self.tag, 
                "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "content": testo, 
                "document_id": self.document.get('document_id')}))
            self.set_save_chunk(docs)
        except Exception as e:
            raise e
    
    def set_save_chunk(self,docs):
        self.del_embeddings()
        try:
            vectorstore = self.create_embeddings(docs)
            if vectorstore:
                self.set_status("completed")
                self.remove_file()
                print(f"end: {datetime.now()}")
            else :
                self.set_status("failed")
                raise ValueError("Vectorstore not found")
                  
        except Exception as e:
            self.set_status("failed")
            raise e