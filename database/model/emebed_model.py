import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .model_general import ModelGeneral
class EmbedModel(ModelGeneral):
    def __init__(self):
        self.table = "vss_chunks"

    def insert_embed(self,data):
       
       if data.get("chunk_id"):
            return self.insert({
                "chunk_id": data.get("chunk_id"),
                "embedding": data.get("embedding"),
            })
       else: 
          return self.insert({
                "query_id": data.get("query_id"),
                "embedding": data.get("embedding"),
            })

    def similarity(self,query_id: int=None, chunk_id:int= None, k:int = 3):
        try:
          select = None
          data   = None
          if chunk_id is not None:
            data = (chunk_id , )
            select = f"""
                     SELECT * FROM chunks c WHERE c.id = (
                     SELECT 
                     chunk_id
                     FROM vss_chunks
                     WHERE embedding MATCH ?
                     AND k = {k}          
                     ORDER BY vec_distance_cosine(embedding, ?) ASC);
                     """
          elif query_id is None:
             data = (query_id , )
             select =f"""
                     SELECT * FROM chunks c WHERE c.id = (
                     SELECT 
                     chunk_id
                     FROM vss_chunks
                     WHERE embedding MATCH (SELECT t.embedding FROM vss_chunks t WHERE t.query_id = ?)
                     AND k = {k}           
                     ORDER BY vec_distance_cosine(embedding, (SELECT t.embedding FROM vss_chunks t WHERE t.query_id = ?)) ASC);
                     """          
          if select is not None:
            return self.statment(query=select,data=data,fetch=True)
          else:
            raise Exception("Query request is wrong") 
        except Exception as e:
          raise e            