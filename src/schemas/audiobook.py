from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class AudiobookCreate(BaseModel):
    title: str = Field(..., description="The title of the audiobook.", example="The Great Gatsby")
    author: str = Field(..., description="The author of the audiobook.", example="F. Scott Fitzgerald")
    duration: int = Field(..., description="The duration of the audiobook in minutes.", example=300)
    cover_image_url: Optional[str] = Field(None, description="The URL of the audiobook's cover image. This field is optional.", example="http://example.com/gatsby.jpg")

class AudiobookUpdate(BaseModel):
    title: Optional[str] = Field(None, description="The new title of the audiobook, if it needs to be updated.", example="The Great Gatsby: Special Edition")
    author: Optional[str] = Field(None, description="The new author of the audiobook, if it needs to be updated.", example="Fitzgerald, F. Scott")
    duration: Optional[int] = Field(None, description="The new duration of the audiobook in minutes, if it needs to be updated.", example=350)
    is_available: Optional[bool] = Field(None, description="Indicates whether the audiobook is available for borrowing.", example=True)
    cover_image_url: Optional[str] = Field(None, description="The new URL of the audiobook's cover image, if it needs to be updated.", example="http://example.com/gatsby_special.jpg")

class AudiobookResponse(BaseModel):
    id: int = Field(..., description="The ID of the audio book.")
    title: str = Field(..., description="The title of the audiobook.", example="The Great Gatsby")
    author: str = Field(..., description="The author of the audiobook.", example="F. Scott Fitzgerald")
    duration: int = Field(..., description="The duration of the audiobook in minutes.", example=300)
    cover_image_url: str = Field(..., description="The URL of the audiobook's cover image.", example="http://example.com/gatsby.jpg")
    is_available: bool = Field(..., description="Indicates whether the audiobook is available for borrowing.", example=True)
    created_at: datetime = Field(..., description="The date and time when the audiobook was created.", example="2024-10-16T12:00:00Z")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "duration": 300,
                "cover_image_url": "http://example.com/gatsby.jpg",
                "is_available": True,
                "created_at": "2024-10-16T12:00:00Z"
            }
        }
