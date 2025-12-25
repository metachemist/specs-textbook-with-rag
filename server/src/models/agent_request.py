from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from src.utils.helpers import generate_uuid, get_current_timestamp


class AgentRequest(BaseModel):
    """
    Represents a user query submitted to the AI agent; contains the question text and any relevant metadata
    """
    id: str = Field(default_factory=generate_uuid)
    message: str
    timestamp: datetime = Field(default_factory=get_current_timestamp)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "uuid-string",
                "message": "What is a sensor in robotics?",
                "timestamp": "2025-12-25T10:30:00Z",
                "metadata": {}
            }
        }

    def model_post_init(self, __context):
        # Validation: message must not be empty
        if not self.message or len(self.message.strip()) == 0:
            raise ValueError("Message must not be empty")
        
        # Validation: message length must be between 1 and 2000 characters
        if len(self.message) > 2000:
            raise ValueError("Message length must be between 1 and 2000 characters")