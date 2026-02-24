import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .model_general import ModelGeneral
from utility.utility import ExceptionRequest

class TopicChunks(ModelGeneral):
    def __init__(self):
        self.table = "t_topic"
        
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

       

