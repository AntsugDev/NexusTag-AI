import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .model_general import ModelGeneral
from utility.utility import ExceptionRequest

class StatusFile(ModelGeneral):
    def __init__(self):
        self.table = "t_status_file"
        
    def create(self,name:str):
        return self.insert({"name":name}) 

    def get_all(self):
        return self.global_search()    

    def get_by_name(self,name:str):
        return self.search({"name":name})

    def get_by_id(self,id:int):
        return self.show(id)

    def update(self,id:int,name:str):
        return self.update({"name":name}, id)

    def delete(self,id:int):
        return self.delete(id) 

    def basic_data(self):
        try:
            data =[
            {"name":"uploaded"},
            {"name":"processed"},
            {"name":"reprocessed"},
            {"name":"error"}
        ]  
            for item in data:
                self.create(item['name']) 
            return True    
        except Exception as e:
            raise ExceptionRequest(message=f"Errore durante l'inserimento dei dati di base: {e}", status_code=409)       

       

