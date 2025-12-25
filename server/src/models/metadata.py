from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from src.utils.validators import is_valid_url


class Metadata(BaseModel):
    """
    Represents associated information (URL, title, timestamp) that provides context for embeddings
    """
    url: str
    title: str
    source_domain: str
    chunk_index: int
    content_type: str
    created_at: datetime
    tags: Optional[List[str]] = Field(default_factory=list)

    @validator('url')
    def validate_url(cls, v):
        if not is_valid_url(v):
            raise ValueError('URL must be valid')
        return v

    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title must not be empty')
        return v

    @validator('source_domain')
    def validate_source_domain(cls, v):
        if not v.strip():
            raise ValueError('Source domain must not be empty')
        return v

    @validator('tags')
    def validate_tags(cls, v):
        if v is not None:
            for tag in v:
                if not isinstance(tag, str):
                    raise ValueError('All tags must be strings')
        return v