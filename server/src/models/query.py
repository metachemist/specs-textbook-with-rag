from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from src.utils.helpers import generate_uuid, get_current_timestamp


class Query(BaseModel):
    """
    Represents a text query string submitted for retrieval
    """
    id: str = Field(default_factory=generate_uuid)
    text: str
    created_at: datetime = Field(default_factory=get_current_timestamp)
    processed_at: Optional[datetime] = None

    @validator('text')
    def validate_text(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Text must not be empty')
        if len(v) > 2000:
            raise ValueError('Text length must be between 1 and 2000 characters')
        return v