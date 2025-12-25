from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from src.utils.helpers import generate_uuid, get_current_timestamp
from .citation import Citation  # Import the Citation model


class AgentResponse(BaseModel):
    """
    Represents the AI's response to the user; contains the answer text and source citations
    """
    id: str = Field(default_factory=generate_uuid)
    request_id: str
    content: str
    citations: List[Citation] = Field(default_factory=list)
    tool_calls: List[dict] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=get_current_timestamp)
    status: str  # "success", "error", "fallback"

    class Config:
        json_schema_extra = {
            "example": {
                "id": "uuid-string",
                "request_id": "uuid-string",
                "content": "A sensor in robotics is a device that detects and responds to some type of input from the physical environment...",
                "citations": [],
                "tool_calls": [],
                "timestamp": "2025-12-25T10:30:00Z",
                "status": "success"
            }
        }

    def model_post_init(self, __context):
        # Validation: content must not be empty
        if not self.content or len(self.content.strip()) == 0:
            raise ValueError("Content must not be empty")
        
        # Validation: request_id must reference an existing AgentRequest
        # Note: This would be validated at runtime against the database/store
        
        # Validation: status must be one of the allowed values
        if self.status not in ["success", "error", "fallback"]:
            raise ValueError("Status must be one of: success, error, fallback")