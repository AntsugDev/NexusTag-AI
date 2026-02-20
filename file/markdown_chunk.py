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
            ("---", "h_sep1")  ,
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
            global_order = 0  

            if self.get_content:
                for doc in self.docs_by_header:
                    headers = doc.metadata
                    header_context = ""
                    
                    if headers:
                        last_header_value = list(headers.values())[-1]
                        header_context = f"{last_header_value}\n\n"
                    
                    full_text = f"{header_context}{doc.page_content}"

                    splits = splitter.split_text(full_text)
                    
                    for text in splits:
                        header_metadata_json = json.dumps(headers) if headers else None
                        
                        if is_testing:
                            result.append({
                                "order": global_order,
                                "content": text,
                                "metadata": header_metadata_json
                            })
                        else:
                            # Inserimento nel database
                            chunk_data = {
                                "id": self.document_id,
                                "content": text,
                                "order_chunk": global_order,
                                "strategy_chunk": self.strategy_chunk(),
                                "token_count": self.count_tokens(text),
                                "overlap_token": self.standard_overlap,
                                "metadata": json.dumps({
                                    "chunk_order": global_order,
                                    "type": self.type_file,
                                    "char_count": len(text),
                                    "headers": headers
                                })
                            }
                            chunk_record = self.chunks.insert_chunk(chunk_data)
                            if chunk_record:
                                result.append(chunk_record)
                        
                        global_order += 1 
            else:
                raise Exception("Errore durante la lettura del file")
            
            return result
        except Exception as e:
            raise e