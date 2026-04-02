import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from chunks.general_chunck import GeneralChunk
from langchain_text_splitters import  RecursiveCharacterTextSplitter
import base64

class Recursive(GeneralChunk):
    def __init__(self,document:dict, standard_token:int = None):
        super().__init__(document,standard_token)
        separator =["\n", "\r\n"]

        self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=int(self.token),
                chunk_overlap=int(self.overlap),
                length_function=len,
                separators=separator,
                is_separator_regex=False
            )

    def chunk(self):
        try: 
            split = self.splitter.split_text(self.content) 

            for (i,chunk) in enumerate(split):
                self.chunks.insert(data={
                    "document_id" : self.document.get('document_id'),
                    "content": base64.b64encode(chunk.encode("utf-8")).decode("utf-8"),
                    "order_chunk":int(i+1),
                    "strategy_chunk": int(self.get_strategy_chunk("recursive")),
                    "token_count":int(self.count_token(chunk)),
                    "overlap_token":int(self.overlap)
                })
            return split
        except Exception as e:
            raise e
        
        