from pydantic import BaseModel, Field, Json

class AskRequest(BaseModel):
     chunks: list[dict] = Field(..., description="Chunks")
     document_id: int = Field(...,description="Document id")

class AskTryning(BaseModel):
     ask: str = Field(...,description="Query")  
     id_query: int = Field(..., description="Id query")   
     k : int = Field(description="List response number best score", default=3)