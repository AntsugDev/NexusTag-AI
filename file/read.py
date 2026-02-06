import os
import pandas as pd
from simple_chunk import SimpleChunk
from csv_chunck import CsvChunk
from xls_chunck import XlsChunk
import mimetypes
from database.model.documents import Documents

TYPE_FILE = ['txt','log','sql','csv', 'md','pdf', 'doc', 'docs', 'xls', 'xlsx']


class ReadFileCustom:
    @staticmethod
    def get_instance(file_path, user_id): # Metodo statico per "creare" l'oggetto giusto
        # 1. Verifica estensione
        ext = file_path.split('.')[-1].lower()
        if ext not in TYPE_FILE:
            raise Exception("Tipo file non supportato")
        # 2. Registrazione Documento nel DB (Logica che avevi già iniziato)
        doc_model = Documents()
        doc_id = doc_model.insert_file({
            "user_id": user_id,
            "name_file": os.path.basename(file_path),
            "size": os.path.getsize(file_path),
            "status_file": "uploaded"
        })
        # 3. Restituisce la classe specializzata passandogli il doc_id
        match ext:
            case 'txt' | 'log' | 'md':
                return SimpleChunk(file_path, ext, doc_id)
            case 'csv':
                return CsvChunk(file_path, ext, doc_id)
            case 'xls' | 'xlsx':
                return XlsChunk(file_path, ext, doc_id)
            case 'pdf':
                return PdfChunk(file_path, ext, doc_id)

        
    def __verify(self, type):   
        try:
            if type not in TYPE_FILE:
                raise Exception("The type file is not accetable")
            return type
        except Exception as e:
            raise e    