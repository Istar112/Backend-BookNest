from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    user_id: int | None = None
    token_type: str | None = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str