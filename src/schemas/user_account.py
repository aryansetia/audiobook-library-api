from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., description="The unique username of the user.")
    email: EmailStr = Field(..., description="The email address of the user. Must be a valid email format.")
    password: str = Field(..., description="The password for the user's account.")

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "securepassword123"
            }
        }


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, description="The new username of the user.")
    email: Optional[EmailStr] = Field(None, description="The new email address of the user.")

    class Config:
        schema_extra = {
            "example": {
                "username": "johnny_doe",
                "email": "johnny@example.com"
            }
        }


class UserResponse(BaseModel):
    id: int = Field(..., description="The unique identifier of the user.")
    username: str = Field(..., description="The username of the user.")
    email: EmailStr = Field(..., description="The email address of the user.")
    created_at: datetime = Field(..., description="The timestamp when the user was created.")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "created_at": "2024-10-16T12:00:00Z"
            }
        }
