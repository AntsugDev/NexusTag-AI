import pandas as pd
import os
import json
from general_chunck import GeneralChunck

class XlsChunk(GeneralChunck):
    def __init__(self, file, type_file, document_id):
        super().__init__(file, type_file, document_id) 
        # Carichiamo tutte le schede (sheet) per non perdere dati
        self.dict_df = pd.read_excel(self.file, sheet_name=None)

    def chunck(self) -> list[dict]:
        try:
            result = []
            for sheet_name, df in self.dict_df.items():
                header_count = len(df.columns)
                num_rows = self.chunck_size_min if header_count > 10 else self.chunck_size_max 

                for i in range(0, len(df), num_rows):
                    df_chunk = df.iloc[i:i + num_rows]
                    content = df_chunk.to_csv(index=False) # CSV è un buon formato testuale per l'AI
                    
                    result.append({
                        "content": f"Sheet: {sheet_name}\n{content}",
                        "metadata": {
                            "sheet_name": sheet_name,
                            "row_start": i,
                            "row_end": min(i + num_rows, len(df)),
                            "columns": list(df.columns)
                        }
                    })
            return result
        except Exception as e:
            raise e 

if __name__ == "__main__":
    files = os.path.join(__file__.replace('file\\csv_chunck.py',''),'fed-prov-competence.csv')
    if os.path.exists(files):
        c = CsvChunk(files)
        r = c.chunk()
        print(r);                   
    else :
        print("File not found !")