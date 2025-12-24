from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from src.utils.validators import is_valid_url


class URLContent(BaseModel):
    """
    Represents the raw content fetched from a URL
    """
    id: str
    url: str
    raw_content: str
    status_code: int
    content_type: Optional[str] = None
    fetched_at: datetime
    encoding: Optional[str] = None
    error_message: Optional[str] = None

    @validator('url')
    def validate_url(cls, v):
        if not is_valid_url(v):
            raise ValueError('URL must be valid')
        return v

    @validator('status_code')
    def validate_status_code(cls, v):
        if not (100 <= v < 600):
            raise ValueError('Status code must be a valid HTTP status code')
        return v

    @validator('raw_content')
    def validate_raw_content(cls, v, values):
        # raw_content must not be empty when status_code indicates success
        if 'status_code' in values and 200 <= values['status_code'] < 300 and not v:
            raise ValueError('Raw content must not be empty when status code indicates success')
        return v