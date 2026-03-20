import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from server.controller.controller import Controller
from utility.utility import ExceptionRequest
from utility.utility import *
from models.documents import Documents
from fastapi import Request, Form, UploadFile, Depends, File, Query
from server.auth.auth import verify_token
import shutil

def document_controller():
   c =  Controller(name='document', is_jwt=True)
   router = c.includeRouter()
   d = Documents()

   @router.get("/list")
   def list(request:Request,page: int = Query(1, ge=1), per_page: int = Query(10, ge=1), orderBy: str = Query('created_at'), sort: str = Query('DESC')):
      try:
         data = d.paginate(page=page, per_page=per_page, orderBy=orderBy, sort=sort)
         return c.setResponse(msg="Document list", data=data)
      except Exception as e:
         return c.setResponse(msg=str(e), status_code=500)

   @router.post("/create")
   async def create(file: UploadFile = File(...), argument: str = Form(...),user: dict = Depends(verify_token)):
      try:
        """
        Per il momento il file viene caricato su una directory,
        si deve pensare al db

        """

        upload_dir = os.path.join(os.getcwd(), 'import-data')
        if not os.path.exists(upload_dir):
           os.makedirs(upload_dir)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        last = d.insert_custom({
              "user_id":user.get("id"),
              "name_file": file.filename, 
              "size": file.size, 
              "mime_type":file.content_type,
              "argument":argument, 
        })
         
        return c.setResponse(msg="Document uploaded", data=last)
      except Exception as e:
        return c.setResponse(msg=str(e), status_code=500)     
  
   return router