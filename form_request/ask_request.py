from pydantic import BaseModel, Field, Json

class AskRequest(BaseModel):
     chunks: list[dict] = Field(..., description="Chunks")
     document_id: int = Field(...,description="Document id")