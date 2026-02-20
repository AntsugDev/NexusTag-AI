import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from file.general_chunck import GeneralChunck
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from database.model.chunks_table import ChunkTable
import json

# file log, txt, markdown e sql
class MarkDownChunk(GeneralChunck):
    def __init__ (self, file, type_file, document_id):
        super().__init__(file, type_file, document_id)
        self.get_content = None
        with open(self.file, 'r',  encoding='utf-8') as f:
            self.get_content = f.read()
        
        self.separator_standard = ["\n", "\r\n"]
        self.chunks = ChunkTable()

        self.header_split = [
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h2"),
            ("---", "h_sep1")  
            ("***", "h_sep2")  
        ]

        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=self.header_split)
        self.docs_by_header    = markdown_splitter.split_text(self.get_content)    

    def chunck(self, is_testing:bool=False) -> list[dict]:
        try:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.standard_token,
                chunk_overlap=self.standard_overlap, 
                length_function=len,
                separators=self.separator_standard,
                is_separator_regex=False
            )
            result = []
            if self.get_content:
                for doc in self.docs_by_header:
                    splits = splitter.split_text(doc)
                    for i, text in enumerate(splits):
                        if is_testing:
                            result.append({
                        "order": i,
                        "content": text,
                        "metadata":None
                       })
                        else:
                            chunk = self.chunks.insert_chunk({
                                        "id": self.document_id,
                                        "content": text,
                                        "order_chunk": i,
                                        "strategy_chunk": self.strategy_chunk(),
                                        "token_count": self.count_tokens(text),
                                        "overlap_token": self.standard_overlap,
                                        "metadata": json.dumps({
                                            "chunk_order": i,
                                            "type": self.type_file,
                                            "char_count": len(text)
                                        })
                                    })
                        if chunk:
                            result.append(chunk)
            else:
                raise Exception("Errore durante la lettura del file")
            return result
        except Exception as e:
            raise e