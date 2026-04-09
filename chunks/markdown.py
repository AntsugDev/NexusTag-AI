import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from chunks.general_chunck import GeneralChunk
from langchain_text_splitters import  MarkdownHeaderTextSplitter, Language
import base64

class Markdown(GeneralChunk):
    def __init__(self,document:dict,loader,tag:str,token:int = None):
        super().__init__(document,loader,tag,token)
        separator = [
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ]

        self.splitter = MarkdownHeaderTextSplitter(
                headers_to_split_on=separator
            )

    def chunk(self):
        try: 
            split = self.splitter.split_text(self.content) 
            self.save_chunk(split)
        except Exception as e:
            raise e