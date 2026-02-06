import pandas as pd
import os
import json
from general_chunck import GeneralChunck

class CsvChunk(GeneralChunck):
    def __init__(self, file, type_file, document_id):
        super().__init__(file, type_file, document_id) 
        self.df = pd.read_csv(self.file)
        self.header_count = len(self.df.columns)
       

    def chunck(self) -> list[dict]:
        try:
            result = []
            # num_rows_per_chunk determina quante righe mettere in un chunk
            num_rows = self.chunck_size_min if self.header_count > 10 else self.chunck_size_max 

            for i in range(0, len(self.df), num_rows):
                df_chunk = self.df.iloc[i:i + num_rows]
                # Convertiamo il subset in stringa per l'embedding
                content = df_chunk.to_csv(index=False) 
                
                result.append({
                    "content": content,
                    "metadata": {
                        "row_start": i,
                        "row_end": min(i + num_rows, len(self.df)),
                        "columns": list(self.df.columns)
                    }
                })
            return result
        except Exception as e:
            raise e 

if __name__ == "__main__":
    files = os.path.join(__file__.replace('file\\csv_chunck.py',''),'fed-prov-competence.csv')
    if os.path.exists(files):
        c = CsvChunk(files, "csv", "doc_123") # Added dummy type_file and document_id
        r = c.chunck() # Renamed method call
        print(r);                   
    else :
        print("File not found !")