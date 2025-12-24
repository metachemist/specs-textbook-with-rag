from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from src.utils.helpers import get_current_timestamp
from src.utils.validators import is_valid_url


class SearchMetadata(BaseModel):
    """
    Represents associated information (Source URL, File Path) that provides context for retrieved chunks
    """
    source_url: str
    source_file_path: str
    title: str
    source_domain: str
    chunk_index: int
    content_type: str = "unknown"
    created_at: datetime = Field(default_factory=get_current_timestamp)
    tags: List[str] = Field(default_factory=list)

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

    @validator('title')
    def validate_title(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Title must not be empty')
        return v

    @validator('source_domain')
    def validate_source_domain(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Source domain must not be empty')
        return v

    @validator('tags')
    def validate_tags(cls, v):
        if v is not None:
            for tag in v:
                if not isinstance(tag, str) or len(tag.strip()) == 0:
                    raise ValueError('All tags must be non-empty strings')
        return v