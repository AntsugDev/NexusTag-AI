import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .model_general import ModelGeneral
from utility.utility import ExceptionRequest

class StrategyChunk(ModelGeneral):
    def __init__(self):
        self.table = "t_strategy_chunk"
        
    def create(self,name:str):
        return self.insert({"name":name}) 

    def get_all(self):
        return self.global_search()    

    def get_by_name(self,name:str):
        search = self.search(data={"name":name}, columns=["id"])
        if search:
            return dict(search[0]).get('id')
        else:
            raise ExceptionRequest(message=f"Strategy not found", status_code=404)    

    def get_by_id(self,id:int):
        return self.show(id)

    def update(self,id:int,name:str):
        return self.update({"name":name}, id)

    def delete(self,id:int):
        return self.delete(id)    

    def _get_id(self,name:str):
        try:
            response =  self.search({"name":name})
            if response:
                return dict(response[0]).get('id')
            else:
                raise ExceptionRequest(message=f"Strategy not found", status_code=404)
        except Exception as e:
            raise ExceptionRequest(message=f"Errore durante il recupero dell'id: {e}", status_code=409)
    def basic_data(self):
        try:
            data =[
            {"name":"testi, logici, sql"},
            {"name":"markdown"},
            {"name":"csv e excel"},
            {"name":"world e pdf"},
            {"name":"generico(non definito)"}
        ]  
            for item in data:
                self.create(item['name']) 
            return True    
        except Exception as e:
            raise ExceptionRequest(message=f"Errore durante l'inserimento dei dati di base: {e}", status_code=409)
       

