from pydantic import BaseModel, Field, Json

class AskRequest(BaseModel):
     chunks: list[str] = Field(..., description="Chunks")