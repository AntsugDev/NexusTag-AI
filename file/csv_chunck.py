import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from file.general_chunck import GeneralChunck
import pandas as pd
import json
import csv
from database.model.chunks_table import ChunkTable


class CsvChunk(GeneralChunck):
    def __init__(self, file, type_file, document_id):
        super().__init__(file, type_file, document_id) 
        self.isExcel = False
        self.isHeader = False
        self.header = None
        try:
            self.excel = pd.ExcelFile(self.file)
            self.isExcel = True
            #self.df = pd.read_excel(self.excel, sheet_name=0,header=None)
        except Exception:
            self.isHeader = self.is_header_csv()
            self.df = pd.read_csv(self.file, header=0 if self.isHeader else None)
        self.header_count = len(self.df.columns)
        self.chunks = ChunkTable()

    def is_header_csv(self):
        try:
            df_preview = pd.read_csv(self.file, nrows=2, header=None)
            row1 = df_preview.iloc[0]
            self.header = list(row1)
            # Metodo 1: Sniffer (molto efficace con stringhe)
            with open(self.file, 'r', encoding='utf-8') as f:
                sample = f.read(2048)
                if csv.Sniffer().has_header(sample):
                    return True

            # Metodo 2: Heuristic (confronto tipi riga 1 vs riga 2)
           
            if len(df_preview) < 2:
                return False
        
           
            row2 = df_preview.iloc[1]
        
            r1_numeric = pd.to_numeric(row1, errors='coerce').notnull().sum()
            r2_numeric = pd.to_numeric(row2, errors='coerce').notnull().sum()
        
            if r2_numeric > r1_numeric:
              return True
            return False
        except Exception:
          return False       

    def chunck(self, is_testing:bool=False) -> list[dict]:
        try:
            # Assicuriamoci che i nomi delle colonne siano stringhe (evita tuple come ('name',))
            self.df.columns = [str(c[0]) if isinstance(c, tuple) else str(c) for c in self.df.columns]
            
            result = []
            num_rows = self.chunck_size_min if self.header_count > 10 else self.chunck_size_max 
            count = 0
            
            for i in range(0, len(self.df), num_rows):
                df_chunk = self.df.iloc[i:i + num_rows].copy()
                json_chunk = df_chunk.astype(object).where(pd.notna(df_chunk), None).to_json(orient="records")
                if is_testing:
                    chunk = self.chunks.insert_chunk({
                        "id": self.document_id,
                        "content": json_chunk,
                        "order_chunk": count,
                        "strategy_chunk": self.strategy_chunk(),
                        "token_count": self.standard_token,
                        "overlap_token": self.standard_overlap,
                        "metadata": json.dumps({
                            "chunk_order": count,
                            "type": self.type_file,
                            "count_row": num_rows
                         })
                        })
                    if chunk:
                        result.append(chunk)
                else :    
                    result.append({
                    "order": count,
                    "content": json_chunk,
                    })
                count += 1
            return result
        except Exception as e:
            raise e
