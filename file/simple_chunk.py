import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from file.general_chunck import GeneralChunck
from langchain_text_splitters import  RecursiveCharacterTextSplitter
from database.model.chunks_table import ChunkTable
import json

# file log, txt, markdown e sql
class SimpleChunk(GeneralChunck):
    def __init__ (self, file, type_file, document_id):
        super().__init__(file, type_file, document_id)
        self.get_content = None
        with open(self.file, 'r',  encoding='utf-8') as f:
            self.get_content = f.read()
        
        self.separator_standard = ["\n", "\r\n"]
        self.chunks = ChunkTable()

        if self.type_file == 'md':
            self.separator_standard = ["#", "##", "###",  "\n", " "]
        elif self.type_file == 'sql':
            self.get_content = self.get_content.upper()
            self.separator_standard = ["SELECT", "UPDATE", "INSERT", "DELETE","CREATE","TABLE","ALTER","DROP","VIEW","PROCEDURE","FUNCTION", "\r\n", "\n"]
            self.setToken(300)

    def chunck(self, is_testing:bool=False) -> list[dict]:
        try:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.standard_token,
                chunk_overlap=self.standard_overlap, # Usiamo la variabile calcolata
                length_function=len,
                separators=self.separator_standard,
                is_separator_regex=False
            )
            result = []
            if self.get_content:
                splits = splitter.split_text(self.get_content)
                for i, text in enumerate(splits):
                   if is_testing:
                       result.append({
                        "order": i,
                        "content": text
                       })
                   else:
                       chunk = self.chunks.insert_chunk({
                        "id": self.document_id,
                        "content": text,
                        "order_chunk": i,
                        "strategy_chunk": self.strategy_chunk(),
                        "token_count": self.standard_token,
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