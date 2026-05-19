from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class AuthorBase(BaseModel):
    name_author: str
    country: str
    image : str

class AuthorDb(AuthorBase):
    id: int
