from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserRequest(BaseModel):
    username: str = Field(..., example="username",description="Username")
    password: str =  Field(..., example="password",description="Password")

class PasswordUpdate(BaseModel):
    password: str  =  Field(..., example="password",description="Password")  