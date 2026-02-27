from pydantic import BaseModel
from fastapi.responses import JSONResponse,Response
import datetime
from sqlite3 import Row
class ExceptionRequest(Exception):
    def __init__(self, message: str = "Errore generico", status_code: int = 400):
        self.message = str(message)
        self.status_code = status_code
        super().__init__(self.message)




def convert_from_pydantic(data):
     if isinstance(data, BaseModel) or isinstance(data, Row):
        return dict(data)
     elif isinstance(data, list):
        return [convert_from_pydantic(item) for item in data]
     elif isinstance(data, dict):
        return {k: convert_from_pydantic(v) for k, v in data.items()}
     else:
      raise TypeError(f"Expected BaseModel instance, got {type(data)}")

def response(msg:str, data: dict=None, status_code:int = 200):
   if status_code == 204 or status_code == 202:
      return Response()

   return JSONResponse(
      content={
         "message": msg,
         "time": datetime.datetime.now().isoformat(),
         "result": data
      },
      status_code=status_code
   )      