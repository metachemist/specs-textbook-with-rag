from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from src.utils.validators import is_valid_url


class CleanText(BaseModel):
    """
    Represents the processed text after cleaning and normalization
    """
    id: str  # Reference to the URLContent ID
    clean_content: str
    original_url: str
    word_count: int
    character_count: int
    cleaned_at: datetime
    processing_notes: Optional[str] = None

    @validator('clean_content')
    def validate_clean_content(cls, v):
        if not v.strip():
            raise ValueError('Clean content must not be empty')
        return v

    @validator('word_count', 'character_count')
    def validate_counts(cls, v):
        if v < 0:
            raise ValueError('Counts must be non-negative')
        return v

    @validator('original_url')
    def validate_original_url(cls, v):
        if not is_valid_url(v):
            raise ValueError('Original URL must be valid')
        return v

    @validator('original_url')
    def validate_url_match(cls, v, values):
        # Note: We can't fully validate URL match here since we don't have access to the referenced URLContent
        # This validation would happen at the application level
        return v