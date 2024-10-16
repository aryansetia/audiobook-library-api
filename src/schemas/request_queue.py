from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class RequestQueueCreate(BaseModel):
    audiobook_id: int
    user_id: int

class RequestQueueResponse(BaseModel):
    audiobook_id: int
    user_id: int
    request_date: datetime

    class Config:
        orm_mode = True

class RequestQueueListResponse(BaseModel):
    queue: List[RequestQueueResponse]
