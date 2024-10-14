from pydantic import BaseModel
from typing import Optional
from datetime  import datetime

class LendCreate(BaseModel):
    audiobook_id: int
    user_id: int
    due_date: datetime

class LendingResponse(BaseModel):
    id: int
    audiobook_id: int
    user_id: int
    borrowed_at: datetime
    due_date: datetime
    is_returned: bool

    class Config:
        orm_mode = True