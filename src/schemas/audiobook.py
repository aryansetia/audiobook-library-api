from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class AudiobookCreate(BaseModel):
    title: str
    author: str
    duration: int
    cover_image_url: Optional[str] = None

class AudiobookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    duration: Optional[str] = None
    cover_image_url: Optional[str] = None

class AudiobookResponse(BaseModel):
    title: str
    author: str
    duration: int
    cover_image_url: str
    is_available: bool
    created_at: datetime

