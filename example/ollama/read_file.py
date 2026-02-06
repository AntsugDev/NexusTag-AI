import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ragdb import RagDb
import json
import mimetypes
import ollama
import numpy as np

class ReadFile:
    def __init__(self):
        self.ragdb = RagDb()
        pass
    
    def read_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(e)
            return None

    def chunking_markdown(self, text):
        try:
            lines = text.split('\n')
            chunks = []
            current_chunk = []
    
            for line in lines:
                # Se trovo un nuovo header (titolo che inizia con #)
                if line.strip().startswith('#'):
                    # Salvo il chunk precedente se non è vuoto
                    if current_chunk:
                        chunks.append('\n'.join(current_chunk).replace('#', '').replace("\n","").strip())
                    # Inizio un nuovo chunk con questo header
                    current_chunk = [line.replace('#', '').replace("\n","").strip()]
                else:
                    # Aggiungo la riga al chunk corrente
                    current_chunk.append(line.replace('#', '').replace("\n","").strip())
    
            # Aggiungo l'ultimo chunk
            if current_chunk:
                chunks.append('\n'.join(current_chunk).replace('#', '').replace("\n","").strip())
    
            return chunks
        except Exception as e:
            print(e)
            return None

    def embedding_text(self, chunks, metadata):
        try:
            for i,chunk in enumerate(chunks):
                print(f"Row {i} wait ollama convert ...")
                olresponse = ollama.embed(
                    model='llama3',
                    input=chunk
                )
                emb = np.array(olresponse.embeddings)
                print(f"chunk {i} convert success")
                self.ragdb.insert_document(metadata['tag'], metadata['file_name'], chunk,json.dumps(emb.tolist()), (i+1), metadata)
        except Exception as e:
            raise e
        return None 

           


if __name__ == "__main__":
    read_file = ReadFile()
    file_path = os.path.join(os.path.dirname(__file__), 'RAG_pipeline_reale.md')
    chunck = read_file.chunking_markdown(read_file.read_file(file_path))
    mimetype, encoding = mimetypes.guess_type(file_path)
    metadata = {
        'tag': 'RAG_pipeline_reale',
        'file_name': 'RAG_pipeline_reale.md',
        'size': os.path.getsize(file_path),
        'mine_type':mimetype,
        'encoding':encoding
    }
    print(f"Chunck create, len :{len(chunck)}")
    print(f"Metadata: {metadata}")

    read_file.embedding_text(chunck, metadata)