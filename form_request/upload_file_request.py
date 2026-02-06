

from pydantic import BaseModel, Field
from fastapi import UploadFile, File

class UploadFileRequest(BaseModel):
    file: UploadFile = File(...)