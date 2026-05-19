from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class BookBase(BaseModel):
    isbn: str 
    title :str
    category : str
    total_pages : int
    publication_date : date
    purchased : bool
    cover_image: Optional[str] = None
    desired:bool = False

class BookDb(BookBase):
    id:int

class BookUpdate(BaseModel):
    isbn: Optional[str]
    title: Optional[str]
    category: Optional[str]
    total_pages: Optional[int]
    publication_date: Optional[date]
    purchased: Optional[bool]
    cover_image: Optional[str]

class Book_authorDb(BaseModel):
    id: int
    id_book: int
    id_author: int