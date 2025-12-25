from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
from src.utils.validators import is_valid_url


class TextChunk(BaseModel):
    """
    Represents a segment of processed content with preserved semantic meaning
    """
    id: str  # Unique identifier for the chunk (UUID)
    content: str
    url: str
    chunk_index: int
    token_count: int
    hash: str  # Content hash for idempotency checks
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @validator('content')
    def validate_content(cls, v):
        if not v.strip():
            raise ValueError('Content must not be empty')
        return v

    @validator('content')
    def validate_content_length(cls, v):
        # Note: This is a simplified validation. In practice, you'd check token count
        if len(v) < 10:
            raise ValueError('Content length must be at least 10 characters')
        return v

    @validator('url')
    def validate_url(cls, v):
        if not is_valid_url(v):
            raise ValueError('URL must be valid')
        return v

    @validator('token_count')
    def validate_token_count(cls, v):
        if v <= 0:
            raise ValueError('Token count must be positive')
        return v

    @validator('hash')
    def validate_hash(cls, v):
        # This is a simplified validation - a real implementation would check SHA-256 format
        if len(v) < 10:  # Minimum length check
            raise ValueError('Hash must be a valid hash string')
        return v