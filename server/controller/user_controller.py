import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fastapi import APIRouter, HTTPException, Request, File, Form, UploadFile, BackgroundTasks, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from form_request.user_request import UserRequest,PasswordUpdate
from database.model.users import User
from utility.utility import convert_from_pydantic, ExceptionRequest, response
from server.auth import create_token

def user_controller(user_router):

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
            raise ExceptionRequest(message=str(e), status_code=422) 

    @user_router.put("/update/{id}",tags=["user"],)
    def update_password(data:PasswordUpdate, id:int):
        try:
            convert = convert_from_pydantic(data)
            user = User()
            result =  user.update_password(id, convert.get('password'))
            return response(msg="Update password success", status_code=202)
        except (Exception, HTTPException, RequestValidationError) as e:
            raise ExceptionRequest(message=e, status_code=422) 

    