from pydantic import BaseModel, Field
from typing import Optional

class ProfileResponse(BaseModel):
    username: str

class ProfileUpdateRequest(BaseModel):
    username: str = Field(..., min_length=3)
    new_password: Optional[str] = Field(default=None, min_length=6)