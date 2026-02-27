from pydantic import BaseModel, Field, Json
from typing import Optional, Any
from datetime import datetime

class JsonEvaluation(BaseModel):
    chunk_id: int = Field(..., description="Chunk ID")
    rating: float = Field(..., description="Rating")

class EvaluationsRequest(BaseModel):
    document_id: int = Field(..., description="Document ID")
    total_chunks: int = Field(..., description="Total chunks")
    avg_tokens: float = Field(..., description="Average tokens")
    total_token: int = Field(..., description="Total token")
    evalutation_for_row: list[JsonEvaluation] = Field(..., description="Evalutation for row")
    total_evaluation: float = Field(..., description="Total evaluation")