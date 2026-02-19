import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def execute_change(ext:str, file_path:str):
    print(f"Stiamo procendo con un file di tipo {ext}")
    match ext:
        case 'txt' | 'log' | 'md' |'sql':
             
             from file.simple_chunk import SimpleChunk
             chunk = SimpleChunk(file_path, ext, None)
             return  chunk.chunck(is_testing=True)
        case 'csv' | 'xls' | 'xlsx':
            from file.csv_chunck import CsvChunk
            chunk = CsvChunk(file_path, ext, None)
            return  chunk.chunck(is_testing=True)     

def create_csv(name:str):
   if os.path.exists(f"{name}_chunk_testing.csv"):
    os.remove(f"{name}_chunk_testing.csv")
   output_path = os.path.join(os.path.dirname(__file__), f"{name}_chunk_testing.csv")
   import pandas as pd
   df = pd.DataFrame(response)
   df.to_csv(output_path,sep=";",header=["order","content","metadata"], index=False)

def extract_data_file(file_path:str,file_request:str):
    try:
        ext = file_path.split('.')[-1].lower()
        name = os.path.splitext(file_request)[0]
        return ext,name
    except Exception as e:
        raise e


try:
    print("-"*30+"CHUNCK TESTING FILE"+"-"*30+"\n")

    file_request = input("Inserisci il nome del file:")
    file_path    = os.path.join('import-data', file_request)
    
    if os.path.exists(file_path):
        print(f"File esiste: {file_path}, procedo con la creazione dei chuncks")

        ext,name = extract_data_file(file_path,file_request)
        response = execute_change(ext,file_path)
        
        if response:
            print(f"File chunckato con successo {name}.{ext}")
            create_csv(name)
        else:
           raise Exception(f"Non è stato possibile creare i chunck per questo file {file_path} ")

    else:
        print(f"File non esiste: {file_path}")   
    
    print("-"*60)
except Exception as e:
    print(f"Errore: {e}") 
    raise e  

