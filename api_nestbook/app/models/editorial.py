from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class EditorialBase(BaseModel):
    name_editorial: str

class EditorialDb(EditorialBase):
    id: int