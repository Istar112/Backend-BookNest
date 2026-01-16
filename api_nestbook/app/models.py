from pydantic import BaseModel
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

#UPDATE USER

class UserUpdate(UserIn):
    name: str
    email:str
    phone: str


# BOOKS
class BookBase(BaseModel):
    isbn: str 
    title :str
    category : str
    total_pages : int
    publication_date : date
    purchased : bool
    cover_image: Optional[str] = None


class BookDb(BookBase):
    id:int

# AUTHOR
class AuthorBase(BaseModel):
    name_author: str
    country: str
    image : str


class AuthorDb(AuthorBase):
    id: int


# STATUS

class StatusUpdate(BaseModel):
    status_str:str
    
class StatusDb(BaseModel):
    id: int


# EDITORIAL
class EditorialBase(BaseModel):
    name_editorial: str


class EditorialDb(EditorialBase):
    id: int

# READING
class ReadingBase(BaseModel):
    id_user:int
    id_book: int
    id_status: int
    reading_status: str


class ReadingDb(ReadingBase):
    id: Optional[int] = None # Autoincrement en la bbdd
    

# BOOK- AUTOR
class Book_authorDb(BaseModel):
    id: int
    id_book: int
    id_author: int


# CLASES QUE HEREDAN DE STATUS ?

class Process(BaseModel):
    id: int
    num_pag: int
    date_start: date


class Finished(BaseModel):
    id: int
    finish_date: date
    rating: Optional[int] = None


class Desired(BaseModel):
    id: int
    comment: Optional[str] = None


