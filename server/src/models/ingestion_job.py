from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from src.utils.validators import is_valid_url


class IngestionJob(BaseModel):
    """
    Represents a single execution of the ingestion process with status tracking
    """
    id: str  # Unique identifier for the ingestion job (UUID)
    status: str  # Current status of the job
    urls_to_process: List[str]  # List of URLs to process in this job
    total_urls: int  # Total number of URLs to process
    processed_urls: int  # Number of URLs processed so far
    successful_chunks: int  # Number of chunks successfully embedded
    failed_chunks: int  # Number of chunks that failed to process
    start_time: datetime  # When the job started
    end_time: Optional[datetime] = None  # When the job completed (if finished)
    error_log: Optional[List[Dict[str, Any]]] = Field(default_factory=list)  # List of errors that occurred during processing

    @validator('status')
    def validate_status(cls, v):
        valid_statuses = [
            "pending", "fetching", "cleaning", "chunking", "embedding", "storing", "completed", "failed"
        ]
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of {valid_statuses}')
        return v

    @validator('total_urls', 'processed_urls', 'successful_chunks', 'failed_chunks')
    def validate_counts(cls, v):
        if v < 0:
            raise ValueError('Counts must be non-negative')
        return v

    @validator('processed_urls')
    def validate_processed_urls(cls, v, values):
        if 'total_urls' in values and v > values['total_urls']:
            raise ValueError('Processed URLs cannot exceed total URLs')
        return v

    @validator('urls_to_process')
    def validate_urls(cls, v):
        for url in v:
            if not is_valid_url(url):
                raise ValueError(f'URL {url} must be valid')
        return v

    @validator('successful_chunks', 'failed_chunks')
    def validate_chunk_counts(cls, v, values):
        if 'processed_urls' in values:
            # This is a simplified validation - in a real implementation, you'd track chunks per URL
            pass
        return v