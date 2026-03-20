from fastapi.responses import JSONResponse,Response
import datetime
import hashlib


class ExceptionRequest(Exception):
    def __init__(self, message: str = "Errore generico", status_code: int = 400):
        self.message = str(message)
        self.status_code = status_code
        super().__init__(self.message)

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

def hash_string(input_string, algorithm='sha256'):
    hash_func = getattr(hashlib, algorithm)()
    hash_func.update(input_string.encode('utf-8'))
    return hash_func.hexdigest()

def verify_string(input_string, hash_to_check, algorithm='sha256'):
    new_hash = hash_string(input_string, algorithm)
    return new_hash == hash_to_check   