from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# READING
class ReadingBase(BaseModel):
    id_user:int
    id_book: int
    id_status: int
    reading_status: str

class ReadingDb(ReadingBase):
    id: Optional[int] = None 
    
class StatusUpdateProcess(BaseModel):
    num_pag: Optional[int] = Field(None, ge=0) 
    date_start: Optional[date] = None

class StatusUpdateFinished(BaseModel):   
    finish_date: Optional[date] = None
    rating: Optional[int] = Field(None, ge=1, le=5)

class StatusDb(BaseModel):
    id: int

class Process(BaseModel):
    id: int
    num_pag: int
    date_start: date

class Finished(BaseModel):
    id: int
    finish_date: Optional[date] = None
    rating: Optional[int] = None

class ProcessDb(Process):
    id: Optional[int] = None

class FinishedDb(Finished):
    id: Optional[int] = None

class ProcessOut(BaseModel):
    num_pag: int
    date_start: date

class FinishedOut(BaseModel):
    finish_date: date
    rating: int
