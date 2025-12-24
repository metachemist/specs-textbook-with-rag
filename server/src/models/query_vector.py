from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime
from src.utils.helpers import get_current_timestamp


class QueryVector(BaseModel):
    """
    Represents the vectorized form of a text query
    """
    query_id: str
    vector: List[float]
    model: str = "embed-english-v3.0"
    created_at: datetime = Field(default_factory=get_current_timestamp)

    @validator('vector')
    def validate_vector(cls, v):
        if len(v) != 1024:  # Cohere's embed-english-v3.0 produces 1024-dimensional vectors
            raise ValueError('Vector must have exactly 1024 dimensions for Cohere embeddings')
        return v

    @validator('model')
    def validate_model(cls, v):
        allowed_models = ["embed-english-v3.0", "embed-english-light-v3.0", "embed-multilingual-v3.0", "embed-multilingual-light-v3.0"]
        if v not in allowed_models:
            raise ValueError(f'Model must be one of {allowed_models}')
        return v