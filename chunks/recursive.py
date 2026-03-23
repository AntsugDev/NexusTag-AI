import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from chunks.general_chunck import GeneralChunk
from langchain_text_splitters import  RecursiveCharacterTextSplitter

class Recursive(GeneralChunk):
    def __init__(self,document:dict, standard_token:int = None):
        super().__init__(document,standard_token)
        separator =["\n", "\r\n"]

        self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.token,
                chunk_overlap=self.overlap,
                length_function=len,
                separators=separator,
                is_separator_regex=False
            )

    def chunk(self):
        try: 
            split = self.splitter.split_text(self.content) 
            for (i,chunk) in enumerate(split):
                self.chunks.insert({
                    "document_id" : self.document_id,
                    "content": chunk,
                    "order_chunk":i+1,
                    "strategy_chunk_id": self.get_strategy_chunk("recursive"),
                    "token_count":self.count_token(chunk),
                    "overlap_token":self.overlap,
                    "is_convert_embeded":False
                })
            return split
        except Exception as e:
            raise ValueError(f"Error chunking document: {e}")
        
        