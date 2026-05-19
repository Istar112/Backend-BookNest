from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class UserBase(BaseModel):
    username: str
    password: str

class UserIn(UserBase):
    name: str
    email: str
    phone: str

class UserDb(UserIn):
    id: int

class UserLoginIn(UserBase):
    pass

class UserUpdate(UserIn):
    name: str
    email:str
    phone: str