from pydantic import BaseModel, Field, Json

class AskRequest(BaseModel):
     chunks: list[dict] = Field(..., description="Chunks")