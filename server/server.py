import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fastapi import FastAPI,HTTPException, Depends, APIRouter, Request, File, Form, UploadFile, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
import uvicorn
import dotenv
import shutil
from utility.utility import  ExceptionRequest, response
dotenv.load_dotenv()
from server.controller.base_controller import base_controller
from server.controller.login_controller import login_controller
from server.controller.document_controller import document_controller

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
base_controller(app)
app.include_router(login_controller())
app.include_router(document_controller())