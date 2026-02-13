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
    fileExist = False
    replace = os.path.join(__file__,'..','..','nexus-tag-ai.db')
    if(os.path.exists(replace)):
        fileExist = True
    return response(msg="Health check", data={
        "status": "ok", 
        "Db": fileExist,
    })
user_router = APIRouter(
    prefix="/api/user",
    tags=["user"]
)
documents_router = APIRouter(
    prefix="/api/documents",
    tags=["documents"],
    dependencies=[Depends(verify_token)]  
)

jobs_router = APIRouter(
    prefix="/api/jobs",
    tags=["jobs"],
    dependencies=[Depends(verify_token)]
)

from server.controller.user_controller import user_controller
user_controller(user_router)

from server.controller.documents_controller import documents_controller
documents_controller(documents_router)

from server.controller.jobs_controller import jobs_controller
jobs_controller(jobs_router)


app.include_router(user_router)
app.include_router(documents_router)
app.include_router(jobs_router)

# Serve Frontend
frontend_path = os.path.join(os.getcwd(), "static")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
else:
    @app.get("/")
    def read_root():
        return {"message": "Cannot find frontend"}