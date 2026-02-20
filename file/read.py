import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pandas as pd
from .simple_chunk import SimpleChunk
from .csv_chunck import CsvChunk
from .xls_chunck import XlsChunk
from .markdown_chunk import MarkDownChunk
import mimetypes
from database.model.documents import Documents

TYPE_FILE = ['txt','log','sql','csv', 'md','pdf', 'doc', 'docs', 'xls', 'xlsx']


class ReadFileCustom:
    @staticmethod
    def get_instance(file_path, doc_id): 
        
        ext = file_path.split('.')[-1].lower()
        if ext not in TYPE_FILE:
            raise Exception("Tipo file non supportato")
        print(f"Read file {file_path} and is type: {ext}\n")
        match ext:
            case 'txt' | 'log'  |'sql':
                c = SimpleChunk(file_path, ext, doc_id)
                return c.chunck()
            case 'md':
                c = MarkDownChunk(file_path, ext, doc_id)
                return c.chunck()
            case 'csv':
                c = CsvChunk(file_path, ext, doc_id)
                return c.chunck()
            case 'xls' | 'xlsx':
                c = XlsChunk(file_path, ext, doc_id)
                return c.chunck()
            case 'pdf':
                c = PdfChunk(file_path, ext, doc_id)
                return c.chunck()

        
    def __verify(self, type):   
        try:
            if type not in TYPE_FILE:
                raise Exception("The type file is not accetable")
            return type
        except Exception as e:
            raise e    