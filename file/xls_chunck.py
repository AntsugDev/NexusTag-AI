import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from file.general_chunck import GeneralChunck
import pandas as pd
import json
from database.model.chunks_table import ChunkTable

class XlsChunk(GeneralChunck):
    def __init__(self, file, type_file, document_id):
        super().__init__(file, type_file, document_id) 
        # Carichiamo tutte le schede (sheet) per non perdere dati
        self.dict_df = pd.read_excel(self.file, sheet_name=None)
        self.chunks = ChunkTable()

    def chunck(self, is_testing:bool=False) -> list[dict]:
        try:
            result = []
            count = 0
            for sheet_name, df in self.dict_df.items():
                header_count = len(df.columns)
                num_rows = self.chunck_size_min if header_count > 10 else self.chunck_size_max 

                for i in range(0, len(df), num_rows):
                    df_chunk = df.iloc[i:i + num_rows]
                    content = df_chunk.to_csv(index=False) # CSV è un buon formato testuale per l'AI
                    
                    if is_testing:
                        result.append({
                            "order": count,
                            "content": f"Sheet: {sheet_name}\n{content}",
                            "metadata": json.dumps({
                                "sheet_name": sheet_name,
                                "row_start": i,
                                "row_end": min(i + num_rows, len(df))
                            })
                        })
                    else:
                        chunk = self.chunks.insert_chunk({
                                "id": self.document_id,
                                "content": f"Sheet: {sheet_name}\n{content}",
                                "order_chunk": count,
                                "strategy_chunk": self.strategy_chunk(),
                                "token_count": self.count_tokens(content),
                                "overlap_token": 0,
                                "metadata": json.dumps({
                                    "chunk_order": count,
                                    "type": self.type_file,
                                    "sheet_name": sheet_name,
                                    "row_start": i,
                                    "row_end": min(i + num_rows, len(df))
                                })
                            })
                        if chunk:
                            result.append(chunk)
                    count += 1
            return result
        except Exception as e:
            raise e