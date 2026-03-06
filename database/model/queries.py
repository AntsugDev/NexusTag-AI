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

    def convert_content(self,content):
        try:
          eb = Embed(content, None, None)
          return eb.embed(True)
        except Exception as e:
            raise e         
    
    def set_query(self,data):
        try: 
            document = self.d.select_document(data.get("document_id"))
            topic_id = document.get('topic')
    
            return self.insert(data={
                    "user_id": data.get("user_id"),
                    "query" :data.get("query"),
                    "topic":topic_id,
                    "embedding": self.convert_content(data.get( "query")),
                    "is_evaluation":data.get("is_evaluation")
                    });
        except Exception as e:
          raise e 