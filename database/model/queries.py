import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .model_general import ModelGeneral 
from database.model.documents import Documents
from embed.embed_service import Embed

class Queries(ModelGeneral):
    def __init__(self):
         self.table = "queries"
         self.d = Documents()

    def convert_content(self,content,query_id,document_id):
        try:
          eb = Embed(content=content, query_id=query_id,document_id=document_id)
          return eb.embed(True)
        except Exception as e:
            raise e         
    
    def set_query(self,data):
        try: 
    
            insert =  self.insert(data={
                    "query" :data.get("query"),
                    "document_id":data.get("document_id"),
                    "is_evaluation":data.get("is_evaluation")
                    });
            if insert:
              from database.model.emebed_model import EmbedModel
              e = EmbedModel()
              e.insert_embed({
                "query_id": insert,
                "embedding": self.convert_content(content=data.get("query"),document_id=data.get("document_id"),query_id=insert),
              })     
        except Exception as e:
          raise e 