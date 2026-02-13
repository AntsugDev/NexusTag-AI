import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fastapi import APIRouter, HTTPException, Request, File, Form, UploadFile, BackgroundTasks, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from form_request.user_request import UserRequest,PasswordUpdate
from database.model.users import User
from utility.utility import convert_from_pydantic, ExceptionRequest, response
from server.auth import verify_token
import shutil

def documents_controller(documents_router):
    @documents_router.get("/documents", tags=["documents"], description="Get list documents for user uplaoded")
    def get_user_documents(page: int = 1, limit: int = 10, user: dict = Depends(verify_token)):
        try:
            from database.model.documents import Documents
            doc_model = Documents()
            data =  None
            if user.get('username') != 'admin': 
             data = {"user_id": user.get("id")}

            items = doc_model.paginate(page=page, limit=limit, data=data)
            total = doc_model.count_search(data=data)
            return response(msg="Documents list retrieved", data={
                "items": [dict(item) for item in items],
                "total": total,
                "page": page,
                "limit": limit
            })
        except Exception as e:
            raise ExceptionRequest(message=str(e), status_code=422)


    @documents_router.post('/upload_file',tags=["documents"], description="Upload a file for processing")  
    def upload_file(file: UploadFile = File(...), argument: str = Form(...), user: dict = Depends(verify_token)):
        file_path = None
        try:
            from database.model.documents import Documents
            
            # Percorso di salvataggio
            upload_dir = os.path.join(os.getcwd(), 'import-data')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
                
            file_path = os.path.join(upload_dir, file.filename)
            
            # Salva il file fisicamente
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            documents = Documents()
            last_id = documents.insert_file({
                "user_id": user.get("id"),
                "name_file": file.filename,
                "status_file": "uploaded",
                "mime_type": file.content_type,
                "size": file.size,
                "topic": argument
            })
            return response(msg="File uploaded successfully, wait for processing", data={
                "filename" : file.filename,
                "last_insert_id" : last_id
            })
        except (Exception, HTTPException, RequestValidationError) as e:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
            raise ExceptionRequest(message=str(e), status_code=422) 

    
    @documents_router.get("/documents/{id}/status", tags=["documents"], description="Get document status")
    def get_document_status(id: int, user: dict = Depends(verify_token)):
        try:
            from database.model.documents import Documents
            doc_model = Documents()
            document = doc_model.select_document(id)
            if not document:
                raise HTTPException(status_code=404, detail="Document not found")
            return response(msg="Document status retrieved", data={"status_file": document["status_file"]})
        except Exception as e:
            raise ExceptionRequest(message=str(e), status_code=422)          
    
    @documents_router.get("/documents/{id}/chunks", tags=["documents"], description="List chunks for document")
    def get_chunks(id: int, page: int = 1, limit: int = 10, user: dict = Depends(verify_token)):
        try:
            from database.model.chunks_table import ChunkTable
            chunk_model = ChunkTable()
            items = chunk_model.paginate(page=page, limit=limit, data={"document_id": id})
            total = chunk_model.count_search(data={"document_id": id})
            return response(msg="Chunks retrieved", data={
                "items": [dict(item) for item in items],
                "total": total,
                "page": page,
                "limit": limit
            })
        except Exception as e:
            raise ExceptionRequest(message=str(e), status_code=422)

    @documents_router.get("/suggest_topic", tags=["documents"], description="Get suggestions for topic")
    def suggest_topic(q: str = "", user: dict = Depends(verify_token)):
        try:
            from database.model.documents import Documents
            doc_model = Documents()
            suggestions = []
            if q and len(q.strip()) >= 2:
                items = doc_model.suggest_topics(q.strip())
                suggestions = [item[0] for item in items if item and item[0]]
            return response(msg="Suggestions retrieved", data=suggestions)
        except Exception as e:
            raise ExceptionRequest(message=str(e), status_code=422)        