from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class RetrievedContext(BaseModel):
    """
    Represents the context retrieved by the tool; contains text chunks with source file/chapter information
    """
    query: str
    chunks: List[dict]
    total_chunks_found: int
    retrieval_time_ms: float

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is a sensor in robotics?",
                "chunks": [
                    {
                        "content": "A sensor in robotics is a device that detects and responds to some type of input from the physical environment...",
                        "score": 0.89,
                        "source_url": "https://example.com/docs/sensors",
                        "source_file_path": "/docs/sensors.md",
                        "chunk_index": 1
                    }
                ],
                "total_chunks_found": 1,
                "retrieval_time_ms": 120.5
            }
        }

    def model_post_init(self, __context):
        # Validation: chunks must contain at least 1 item
        if len(self.chunks) < 1:
            raise ValueError("Chunks must contain at least 1 item")
        
        # Validation: total_chunks_found must be >= 0
        if self.total_chunks_found < 0:
            raise ValueError("Total chunks found must be >= 0")
        
        # Validation: retrieval_time_ms must be >= 0
        if self.retrieval_time_ms < 0:
            raise ValueError("Retrieval time must be >= 0")
        
        # Validation: each chunk must have valid content and source information
        for chunk in self.chunks:
            if not chunk.get("content") or len(chunk.get("content", "").strip()) == 0:
                raise ValueError("Each chunk must have valid content")
            if not chunk.get("source_file_path"):
                raise ValueError("Each chunk must have a valid source file path")