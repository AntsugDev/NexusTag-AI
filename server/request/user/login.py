from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username:str = Field(..., description="Username")
    password:str = Field(..., description="Password")