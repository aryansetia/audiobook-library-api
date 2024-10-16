from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class RequestQueueCreate(BaseModel):
    audiobook_id: int = Field(..., description="The unique identifier of the audiobook being requested.")
    user_id: int = Field(..., description="The unique identifier of the user making the request.")

    class Config:
        schema_extra = {
            "example": {
                "audiobook_id": 1,
                "user_id": 2
            }
        }


class RequestQueueResponse(BaseModel):
    audiobook_id: int = Field(..., description="The unique identifier of the audiobook.")
    user_id: int = Field(..., description="The unique identifier of the user in the request queue.")
    request_date: datetime = Field(..., description="The date and time when the request was made.")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "audiobook_id": 1,
                "user_id": 2,
                "request_date": "2024-10-16T12:00:00Z"
            }
        }


class RequestQueueListResponse(BaseModel):
    queue: List[RequestQueueResponse] = Field(..., description="List of requests in the queue for the audiobook.")

    class Config:
        schema_extra = {
            "example": {
                "queue": [
                    {
                        "audiobook_id": 1,
                        "user_id": 2,
                        "request_date": "2024-10-16T12:00:00Z"
                    },
                    {
                        "audiobook_id": 1,
                        "user_id": 3,
                        "request_date": "2024-10-16T13:00:00Z"
                    }
                ]
            }
        }
