import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def execute_change(ext:str, file_path:str, document_id:int):
    print(f"Stiamo procendo con un file di tipo {ext}")
    match ext:
        case 'txt' | 'log' |'sql':
             from file.simple_chunk import SimpleChunk
             chunk = SimpleChunk(file_path, ext, document_id)
             return  chunk.chunck(is_testing=True)
        case 'md':
            from file.markdown_chunk import MarkDownChunk
            chunk = MarkDownChunk(file_path, ext, document_id)
            return  chunk.chunck(is_testing=False)     
        case 'csv' | 'xls' | 'xlsx':
            from file.csv_chunck import CsvChunk
            chunk = CsvChunk(file_path, ext, document_id)
            return  chunk.chunck(is_testing=True)     

def create_csv(name:str):
    if os.path.exists(f"{name}_chunk_testing.csv"):
        os.remove(f"{name}_chunk_testing.csv")
    output_path = os.path.join(os.path.dirname(__file__), f"{name}_chunk_testing.csv")
    import pandas as pd
    df = pd.DataFrame(response)
    
    # Mappiamo le colonne se necessario
    if "order_chunk" in df.columns:
        df = df.rename(columns={"order_chunk": "order"})
        
    cols = ["order", "content", "metadata"]
    available_cols = [c for c in cols if c in df.columns]
    
    if available_cols:
        df[available_cols].to_csv(output_path, sep=";", index=False)
    else:
        df.to_csv(output_path, sep=";", index=False)


def extract_data_file(file_path:str,file_request:str):
    try:
        ext = file_path.split('.')[-1].lower()
        name = os.path.splitext(file_request)[0]
        return ext,name
    except Exception as e:
        raise e


try:
    print("-"*30+"CHUNCK TESTING FILE"+"-"*30+"\n")

    file_request = input("Inserisci il nome del file(il file deve essere in import-data):")
    file_path    = os.path.join('import-data', file_request)
    
    if os.path.exists(file_path):
        print(f"File esiste: {file_path}, procedo con la creazione dei chuncks")

        ext,name = extract_data_file(file_path,file_request)
        from database.model.documents import Documents
        document = Documents()
        search = document.search(data={"name_file": f"{name}.{ext}"}, columns=["id"])
        document_id = None
        if search:
            print(f"Document esiste: {name}.{ext}, procedo con la creazione dei chuncks ... ")
            document_id = dict(search[0])["id"]
       
        response = execute_change(ext,file_path,document_id)
        
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

