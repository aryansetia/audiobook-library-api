from pydantic import BaseModel
from typing import Optional

# Token model to hold the access token
class Token(BaseModel):
    access_token: str
    token_type: str

# Model to represent the token data (sub: user_id)
class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str
