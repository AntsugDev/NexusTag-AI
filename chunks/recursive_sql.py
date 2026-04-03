import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from chunks.general_chunck import GeneralChunk
from langchain_text_splitters import  RecursiveCharacterTextSplitter, Language
import base64

class RecursiveSql(GeneralChunk):
    def __init__(self,document:dict,loader,tag:str,token:int = None):
        super().__init__(document,loader,tag,token)
        separator =["SELECT ", "INSERT ", "UPDATE ", "DELETE ", "CREATE ", "ALTER ", "DROP ", "TRUNCATE ", "\r\n", ";"]

        self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=int(self.token),
                chunk_overlap=int(self.overlap),
                separators=separator
            )

    def chunk(self):
        try: 
            split = self.splitter.split_text(self.content) 
            self.save_chunk(split)
        except Exception as e:
            raise e