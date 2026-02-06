from pydantic import BaseModel
from fastapi.responses import JSONResponse,Response
import datetime

class ExceptionRequest(Exception):
    def __init__(self, message: str = "Errore generico", status_code: int = 400):
        self.message = str(message)
        self.status_code = status_code
        super().__init__(self.message)




def convert_from_pydantic(data):
     if isinstance(data, BaseModel):
        return data.model_dump()
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