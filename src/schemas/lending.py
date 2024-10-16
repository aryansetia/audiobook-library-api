from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LendingCreate(BaseModel):
    audiobook_id: int = Field(..., description="The ID of the audiobook being borrowed.", example=101)
    due_date: Optional[datetime] = Field(None, description="The due date for returning the audiobook. This field is optional.", example="2024-10-23T12:00:00Z")

class LendingResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for the lending record.", example=1)
    audiobook_id: int = Field(..., description="The ID of the audiobook that has been borrowed.", example=101)
    user_id: int = Field(..., description="The ID of the user who borrowed the audiobook.", example=1)
    borrowed_at: datetime = Field(..., description="The date and time when the audiobook was borrowed.", example="2024-10-16T12:00:00Z")
    due_date: datetime = Field(..., description="The date and time by which the audiobook should be returned.", example="2024-10-23T12:00:00Z")
    is_returned: bool = Field(..., description="Indicates whether the audiobook has been returned.", example=False)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "audiobook_id": 101,
                "user_id": 1,
                "borrowed_at": "2024-10-16T12:00:00Z",
                "due_date": "2024-10-23T12:00:00Z",
                "is_returned": False
            }
        }
