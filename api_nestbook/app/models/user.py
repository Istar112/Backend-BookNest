from pydantic import BaseModel
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
    streak_days: Optional[int] = 0
    last_reading_date: Optional[str] = None


class UserLoginIn(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    streak_days: Optional[int] = None
    last_reading_date: Optional[str] = None


class UserOut(BaseModel):
    name: str
    username: str
    email: str
    phone: str


class UserStreakOut(BaseModel):
    streakDays: int
    lastReadingDate: Optional[str] = None


class UserStreakUpdate(BaseModel):
    streak_days: int