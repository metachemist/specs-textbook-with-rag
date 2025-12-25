from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime


class Embedding(BaseModel):
    """
    Represents a vectorized representation of a text chunk
    """
    id: str  # Reference to the TextChunk ID
    vector: List[float]  # The embedding vector (1024 dimensions for Cohere)
    model: str  # The embedding model used (e.g., "embed-english-v3.0")
    created_at: datetime

    @validator('vector')
    def validate_vector(cls, v):
        # For Cohere embeddings, the vector should have 1024 dimensions
        if len(v) != 1024:
            raise ValueError('Vector must have exactly 1024 dimensions for Cohere embeddings')
        return v

    @validator('model')
    def validate_model(cls, v):
        valid_models = [
            "embed-english-v3.0",
            "embed-multilingual-v3.0",
            "embed-english-light-v3.0",
            "embed-multilingual-light-v3.0"
        ]
        if v not in valid_models:
            raise ValueError(f'Model must be one of {valid_models}')
        return v