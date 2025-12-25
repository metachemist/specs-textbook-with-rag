from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from src.utils.helpers import generate_uuid


class Citation(BaseModel):
    """
    Represents the source attribution for information in the agent's response; 
    contains chapter/file reference and possibly page numbers or section titles
    """
    id: str = Field(default_factory=generate_uuid)
    source_file_path: str
    source_url: str
    chapter: Optional[str] = None
    page_number: Optional[int] = None
    text_preview: str
    confidence_score: float = 1.0  # Default to high confidence

    class Config:
        json_schema_extra = {
            "example": {
                "id": "uuid-string",
                "source_file_path": "/docs/sensors.md",
                "source_url": "https://example.com/docs/sensors",
                "chapter": "Sensors and Actuators",
                "text_preview": "A sensor in robotics is a device that detects...",
                "confidence_score": 0.95
            }
        }

    def model_post_init(self, __context):
        # Validation: source_file_path must not be empty
        if not self.source_file_path or len(self.source_file_path.strip()) == 0:
            raise ValueError("Source file path must not be empty")
        
        # Validation: text_preview must not be empty
        if not self.text_preview or len(self.text_preview.strip()) == 0:
            raise ValueError("Text preview must not be empty")
        
        # Validation: confidence_score must be between 0.0 and 1.0
        if not (0.0 <= self.confidence_score <= 1.0):
            raise ValueError("Confidence score must be between 0.0 and 1.0")