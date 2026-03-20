import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from server.controller.controller import Controller
from utility.utility import ExceptionRequest
from server.request.user.login import LoginRequest
from server.auth.auth import create_token
from models.users import Users
from utility.utility import *

def login_controller():
    c = Controller(app=None, is_jwt=False, name="user")
    router = c.includeRouter()
    user = Users()

    @router.post("/login")
    def login(request: LoginRequest):
        try:
            d = request.dict()
            search = user.findBy([{'column': 'username', 'operator': '=', 'value': d['username'],"type":"AND"}])
            if not search:
                raise ExceptionRequest("User not found")
            if not verify_string(d['password'], search[0]['password']):
                raise ExceptionRequest("Invalid password")
            token = create_token(search[0])
            return c.setResponse(msg="Login", data={"token": token}, status_code=200)
        except Exception as e:
            raise ExceptionRequest(e)
    
    @router.post("/register")
    def register(request: LoginRequest):
        try:
            d = request.dict()
            print(d)
            last =user.insert({
                "username": d["username"],
                "password": hash_string(d["password"])
            })
            print(last)
            return c.setResponse(msg="Register", data={"id": last}, status_code=200)
        except Exception as e:
            raise ExceptionRequest(e)
    
    return router
    
    
    