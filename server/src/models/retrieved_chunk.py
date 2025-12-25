from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Optional
from datetime import datetime
from src.utils.helpers import generate_uuid
from src.utils.validators import is_valid_url


class RetrievedChunk(BaseModel):
    """
    Represents a text chunk returned from the vector search with relevance score
    """
    id: str = Field(default_factory=generate_uuid)
    content: str
    score: float
    source_url: str
    source_file_path: str
    chunk_index: int
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @validator('content')
    def validate_content(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Content must not be empty')
        return v

    @validator('score')
    def validate_score(cls, v):
        if not (0.0 <= v <= 1.0):
            raise ValueError('Score must be between 0.0 and 1.0')
        return v

    @validator('source_url')
    def validate_source_url(cls, v):
        if not is_valid_url(v):
            raise ValueError('Source URL must be a valid URL format')
        return v

    @validator('source_file_path')
    def validate_source_file_path(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Source file path must not be empty')
        return v