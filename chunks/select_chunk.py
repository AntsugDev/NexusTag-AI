import os 
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from chunks.recursive import Recursive
from models.documents import Documents
class SelectChunk:
    def __init__(self,document_id:int):
        self.document = Documents().find(document_id)
        if not self.document:
            raise ValueError(f"Document not found: {document_id}")
        
        mime_type = self.document[0].get('mime_type')
        match self.document[0].get('mime_type'):
            case "text/plain" | "application/octet-stream":
                Recursive(self.document[0]).chunk()
            case _:    
                raise ValueError(f"Unsupported mime type: {mime_type}")
            # case "application/pdf":
            # case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                
            # case "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
               
            # case "application/vnd.openxmlformats-officedocument.presentationml.presentation":
                
            #     raise ValueError(f"Unsupported mime type: {mime_type}")
    
    