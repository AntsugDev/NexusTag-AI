import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fastapi import FastAPI,HTTPException, Depends, APIRouter, Request, File, Form, UploadFile, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
import uvicorn
from form_request.user_request import UserRequest,PasswordUpdate
from database.model.users import User
from utility.utility import convert_from_pydantic, ExceptionRequest, response
from server.auth import *
import dotenv
import shutil

dotenv.load_dotenv()

app = FastAPI(
    title="NexusTag AI documentation",
    version="1.0.0",
    description="API documentation for NexusTag AI",
    root_path=os.getenv('HOST_NAME'),
    docs_url="/docs",
    openapi_url="/openapi.json"
)

origins = [
    "http://localhost:5173", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Accept",
        "Origin",
        "X-Requested-With",
        "Access-Control-Allow-Headers",
    ],
    expose_headers=["Content-Disposition"],  
    max_age=600,  
)

@app.exception_handler(ExceptionRequest)
async def global_exception_handler(request: Request, exc: ExceptionRequest):
    if isinstance(exc, ExceptionRequest):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message}
        )
    return JSONResponse(
        status_code=500,
        content={"error": "errore generico"}
    )

@app.get("/health")
def health():
    return {"status": "ok"}


user_router = APIRouter(
    prefix="/api/user",
    tags=["user"]
)

@user_router.get("/documents", tags=["user"])
def get_user_documents(page: int = 1, limit: int = 10, user: dict = Depends(verify_token)):
    try:
        from database.model.documents import Documents
        doc_model = Documents()
        # We need a way to filter by user_id in paginate
        items = doc_model.paginate(page=page, limit=limit, data={"user_id": user.get("id")})
        total = doc_model.count_search(data={"user_id": user.get("id")})
        return response(msg="User documents retrieved", data={
            "items": [dict(item) for item in items],
            "total": total,
            "page": page,
            "limit": limit
        })
    except Exception as e:
        raise ExceptionRequest(message=str(e), status_code=422)

auth_router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
    dependencies=[Depends(verify_token)]  
)

@user_router.post("/register",tags=["user"],)
def register(data:UserRequest):
    try:
        convert = convert_from_pydantic(data)
        user = User()
        register =  user.register(convert.get('username'), convert.get('password'))
        return response(msg="User created", data={
            "last_insert_id" : register
        }, status_code=201)
    except (Exception, HTTPException, RequestValidationError) as e:
        raise ExceptionRequest(message=e, status_code=422) 

@user_router.post("/login",tags=["user"],)
def login(data:UserRequest):
    try:
        convert = convert_from_pydantic(data)
        user = User()
        result =  user.login(convert.get('username'), convert.get('password'))
        if result is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        token = create_token(result)
        return response(msg="Login success", data={
            "access_token": token,
            "username": convert.get('username')
        }, status_code=200)
    except (Exception, HTTPException, RequestValidationError) as e:
        raise ExceptionRequest(message=e, status_code=422) 

@user_router.put("/update/{id}",tags=["user"],)
def login(data:PasswordUpdate, id:int):
    try:
        convert = convert_from_pydantic(data)
        user = User()
        result =  user.update_password(id, convert.get('password'))
        return response(msg="Update password success", status_code=202)
    except (Exception, HTTPException, RequestValidationError) as e:
        raise ExceptionRequest(message=e, status_code=422) 


@auth_router.post('/upload_file',tags=["auth"],)  
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

admin_router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
    dependencies=[Depends(verify_token)]
)

@admin_router.get("/suggest_topic", tags=["admin"])
def suggest_topic(q: str = "", user: dict = Depends(verify_token)):
    if user.get("username") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden: Admin only")
    try:
        from database.model.documents import Documents
        doc_model = Documents()
        suggestions = []
        if q and len(q.strip()) >= 2:
            items = doc_model.suggest_topics(q.strip())
            suggestions = [item[0] for item in items if item and item[0]]
        return response(msg="Suggestions retrieved", data=suggestions)
    except Exception as e:
        return response(msg="No suggestions", data=[])



@admin_router.get("/documents", tags=["admin"])
def get_documents(page: int = 1, limit: int = 10, user: dict = Depends(verify_token)):
    if user.get("username") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden: Admin only")
    try:
        from database.model.documents import Documents
        doc_model = Documents()
        items = doc_model.paginate(page=page, limit=limit)
        total = doc_model.count()
        return response(msg="Documents retrieved", data={
            "items": [dict(item) for item in items],
            "total": total,
            "page": page,
            "limit": limit
        })
    except Exception as e:
        raise ExceptionRequest(message=str(e), status_code=422)

@admin_router.get("/documents/{id}/chunks", tags=["admin"])
def get_chunks(id: int, page: int = 1, limit: int = 10, user: dict = Depends(verify_token)):
    if user.get("username") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden: Admin only")
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

@admin_router.get("/documents/{id}/status", tags=["admin"])
def get_document_status(id: int, user: dict = Depends(verify_token)):
    if user.get("username") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden: Admin only")
    try:
        from database.model.documents import Documents
        doc_model = Documents()
        document = doc_model.select_document(id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return response(msg="Document status retrieved", data={"status_file": document["status_file"]})
    except Exception as e:
        raise ExceptionRequest(message=str(e), status_code=422)

@admin_router.get("/documents/{id}/error", tags=["admin"])
def get_document_error(id: int, user: dict = Depends(verify_token)):
    if user.get("username") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden: Admin only")
    try:
        from database.model.jobs_failed import JobsFailed
        job_failed = JobsFailed()
        error_msg = job_failed.get_last_error(id)
        return response(msg="Error details retrieved", data={"error": error_msg})
    except Exception as e:
        raise ExceptionRequest(message=str(e), status_code=422)

def run_document_processing(id: int, document: dict):
    try:
        from database.model.documents import Documents
        from database.model.chunks_table import ChunkTable
        from file.read import ReadFileCustom
        
        doc_model = Documents()
        chunk_model = ChunkTable()
        
        # 1. Cleanup before starting (Rollback Strategy)
        chunk_model.delete_by_document(id)
        
        # 2. Trigger processing
        worked = ReadFileCustom.get_instance(document["name_file"], document["user_id"])
        
        if worked:
            doc_model.update_processed(id)
        else:
            doc_model.update_error(id)
            from database.model.jobs_failed import JobsFailed
            job_failed = JobsFailed()
            job_failed.insert_job_failed({
                "document_id": id,
                "row_id": 0,
                "meta_data": document,
                "exception": "Processing failed without specific error"
            })
    except Exception as e:
        from database.model.documents import Documents
        Documents().update_error(id)
        try:
            from database.model.jobs_failed import JobsFailed
            JobsFailed().insert_job_failed({
                "document_id": id,
                "row_id": 0,
                "meta_data": document,
                "exception": str(e)
            })
        except:
            pass

@admin_router.post("/documents/{id}/process", tags=["admin"])
def process_document(id: int, background_tasks: BackgroundTasks, user: dict = Depends(verify_token)):
    if user.get("username") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden: Admin only")
    try:
        from database.model.documents import Documents
        doc_model = Documents()
        document = doc_model.select_document(id)
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
            
        # Imposta lo stato a 'processing' (opzionale, se vuoi un nuovo stato)
        # doc_model.update({"status_file": "processing"}, id)
        
        # Avvia in background
        background_tasks.add_task(run_document_processing, id, document)
        
        return response(msg="Processing started in background")
            
    except Exception as e:
        raise ExceptionRequest(message=str(e), status_code=422)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(admin_router)

# Serve Frontend
frontend_path = os.path.join(os.getcwd(), "static")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
else:
    @app.get("/")
    def read_root():
        return {"message": "Frontend not built yet. Run 'npm run build' in the frontend folder."}