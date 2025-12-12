from pydantic import BaseModel
from datetime import date

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


class BookBase(BaseModel):
    isbn: str 
    title :str
    category : str
    total_pages : int
    publication_date : date
    purchased : bool


class BookDb(BookBase):
    id:int

