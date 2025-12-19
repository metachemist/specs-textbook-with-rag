from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class User(BaseModel):
    id: str = str(uuid.uuid4())
    email: str
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()