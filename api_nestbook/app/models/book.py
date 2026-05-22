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
    isbn: Optional[str] = None
    title: Optional[str] = None
    category: Optional[str] = None
    total_pages: Optional[int] = None
    publication_date: Optional[date] = None
    purchased: Optional[bool] = None
    cover_image: Optional[str] = None
    desired: Optional[bool] = None

class Book_authorDb(BaseModel):
    id: int
    id_book: int
    id_author: int