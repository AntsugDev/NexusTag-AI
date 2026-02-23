from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EvaluationsRequest(BaseModel):
    document_id: int = Field(..., description="Document ID")
    avg_score: float = Field(..., description="Average score")
    total_score: float = Field(..., description="Total score")
    random_chunks_evaluation: int = Field(..., description="Number of random chunks evaluation")
    metadata: dict = Field(..., description="Metadata")