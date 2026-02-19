try:
    print("-"*30+"CHUNCK TESTING FILE DI BASICI (TESTO,MD,SQL)"+"-"*30+"\n")
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from file.simple_chunk import SimpleChunk
    DOC_ID = input("Inserisci il nome del file:")
    file_path = os.path.join('import-data', DOC_ID)
    print("Lettura di un file di testo ...")
    if os.path.exists(file_path):
        print(f"File esiste: {file_path}")
        ext = file_path.split('.')[-1].lower()
        name = os.path.splitext(DOC_ID)[0]
        chunk = SimpleChunk(file_path, ext, None)
        response = chunk.chunck(is_testing=True)
        if response:
            print(f"File chunckato con successo {name}.{ext}")
            output_path = os.path.join(os.path.dirname(__file__), f"{name}_chunk_testing.csv")
            import pandas as pd
            df = pd.DataFrame(response)
            df.to_csv(output_path,sep=";",header=["order","content"], index=False)
        else:
            print("File non chunckato")
    else:
        print(f"File non esiste: {file_path}")   
    
    print("-"*60)
except Exception as e:
    print(f"Errore: {e}")   
    raise e
