import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fastapi import FastAPI,HTTPException, Depends, APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
import uvicorn
from form_request.user_request import UserRequest,PasswordUpdate
from database.model.users import User
from utility.utility import convert_from_pydantic, ExceptionRequest, response

app = FastAPI(
    title="Rag read documentation",
    version="1.0.0",
    docs_url="/rag/docs",
    openapi_url="/rag/openapi.json"
)

# origins = [
#     "http://localhost:5173", 
# ]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
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
        return response(msg="Login success", data=result)
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


app.include_router(user_router)

uvicorn.run(app, host="0.0.0.0", port=8081, log_level="info")


