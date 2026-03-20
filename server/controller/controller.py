import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fastapi import Depends, APIRouter
from auth.auth import verify_token
from utility.utility import response

class Controller:
    def __init__(self,app = None, is_jwt=False, name=""):
        self.app = app
        self.baseRouter = f"/api/{os.getenv('API_VERSION')}/{name}"
        
        self.dependencies = []
        if(is_jwt):
            self.dependencies.append(Depends(verify_token))
        self.router =  APIRouter(
            prefix=self.baseRouter,
            tags=[name],
            dependencies=self.dependencies
        ) if app is None else app
    def includeRouter(self):
        return self.router  

    def setResponse(self,msg:str, data: dict=None, status_code:int = 200):
        return response(msg=msg, data=data, status_code=status_code) 

    # def routes_default(self):
    #     r = ['/list', '/create','/delete/{id}','/update/{id}']
    #     return r
            


   

