from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class ChatLog(BaseModel):
    id: str = str(uuid.uuid4())
    user_id: str
    query: str
    response: str
    timestamp: datetime = datetime.now()
    context: Optional[str] = None