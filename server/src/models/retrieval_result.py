from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime
from src.utils.helpers import generate_uuid, get_current_timestamp
from src.models.retrieved_chunk import RetrievedChunk


class RetrievalResult(BaseModel):
    """
    Represents the complete result set with metadata for each chunk
    """
    id: str = Field(default_factory=generate_uuid)
    query_id: str
    chunks: List[RetrievedChunk]
    total_chunks_found: int = 0
    search_time_ms: float = 0.0
    created_at: datetime = Field(default_factory=get_current_timestamp)

    @validator('chunks')
    def validate_chunks(cls, v):
        if not v or len(v) == 0:
            raise ValueError('Chunks must contain at least 1 item')
        if len(v) > 10:
            raise ValueError('Chunks must contain between 1 and 10 items')
        return v

    @validator('total_chunks_found')
    def validate_total_chunks_found(cls, v):
        if v < 0:
            raise ValueError('Total chunks found must be >= 0')
        return v

    @validator('search_time_ms')
    def validate_search_time_ms(cls, v):
        if v < 0:
            raise ValueError('Search time must be >= 0')
        return v