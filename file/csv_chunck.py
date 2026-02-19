import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from file.general_chunck import GeneralChunck
import pandas as pd
import json
import csv
from database.model.chunks_table import ChunkTable


class CsvChunk(GeneralChunck):
    def __init__(self, file, type_file, document_id = None):
        super().__init__(file, type_file, document_id) 
        self.isExcel = False
        self.isHeader = False
        self.header = None
        self.sheets = None
        self.df = None
        
        ext = self.file.split('.')[-1].lower()
        if ext in ['xls', 'xlsx']:
            try:
                self.excel = pd.ExcelFile(self.file)
                self.isExcel = True
                self.sheets = self.excel.sheet_names
            except Exception as e:
                # Se fallisce qui, probabile manchi openpyxl o il file sia corrotto
                print(f"Errore caricamento Excel: {e}")
                raise Exception(f"Impossibile leggere il file Excel. Assicurati che 'openpyxl' sia installato. Errore: {e}")
        else:
            self.isHeader = self.is_header_csv()
            self.df = pd.read_csv(self.file, header=0 if self.isHeader else None)
            self.header_count = len(self.df.columns)
            
        self.chunks = ChunkTable()

    def is_header_csv(self):
        try:
            df_preview = pd.read_csv(self.file, nrows=2, header=None)
            if len(df_preview) < 1:
                return False
                
            row1 = df_preview.iloc[0]
            self.header = list(row1)
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    sample = f.read(2048)
                    if csv.Sniffer().has_header(sample):
                        return True
            except UnicodeDecodeError |Exception:
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

    def set_columns(self, df):
        return [str(c[0]) if isinstance(c, tuple) else str(c) for c in df.columns]  

    def set_num_rows(self, header_count):
        return self.chunck_size_min if header_count > 10 else self.chunck_size_max            

    def chunck(self, is_testing:bool=False) -> list[dict]:
        try:
            result = []
            count = 0
            if self.isExcel:
                for sheet in self.sheets:
                    df_tmp = pd.read_excel(self.excel, sheet_name=sheet, header=0 if self.isHeader else None)
                    header_count = len(df_tmp.columns)
                    df_tmp.columns = self.set_columns(df_tmp)
                    num_rows = self.set_num_rows(header_count)
                    
                    for i in range(0, len(df_tmp), num_rows):
                        df_chunk = df_tmp.iloc[i:i + num_rows].copy()
                        # Usiamo to_json per mantenere la struttura dati serializzata
                        json_content = df_chunk.astype(object).where(pd.notna(df_chunk), None).to_json(orient="records")
                        
                        if not is_testing:
                            chunk = self.chunks.insert_chunk({
                                "id": self.document_id,
                                "content": json_content,
                                "order_chunk": count,
                                "strategy_chunk": self.strategy_chunk(),
                                "token_count": None,
                                "overlap_token": None,
                                "metadata": json.dumps({
                                    "chunk_order": count,
                                    "type": self.type_file,
                                    "count_row": len(df_chunk),
                                    "sheet_name": sheet
                                })
                            })
                            if chunk:
                                result.append(chunk)
                        else:
                            result.append({
                                "order": count,
                                "content": json_content,
                                "metadata": json.dumps({
                                    "sheet_name": sheet
                                })
                            })
                        count += 1
                return result 
            else:
                self.df.columns = self.set_columns(self.df)
                num_rows = self.set_num_rows(self.header_count)
                for i in range(0, len(self.df), num_rows):
                    df_chunk = self.df.iloc[i:i + num_rows].copy()
                    json_content = df_chunk.astype(object).where(pd.notna(df_chunk), None).to_json(orient="records")
                    
                    if not is_testing:
                        chunk = self.chunks.insert_chunk({
                            "id": self.document_id,
                            "content": json_content,
                            "order_chunk": count,
                            "strategy_chunk": self.strategy_chunk(),
                            "token_count": None,
                            "overlap_token": None,
                            "metadata": json.dumps({
                                "chunk_order": count,
                                "type": self.type_file,
                                "count_row": len(df_chunk)
                            })
                        })
                        if chunk:
                            result.append(chunk)
                    else:
                        result.append({
                            "order": count,
                            "content": json_content,
                            "metadata": None
                        })
                    count += 1
                return result 
        except Exception as e:
            raise e