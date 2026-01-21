# imports
from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from app.models import *
from app.database import *    
from app.auth.auth import oauth2_scheme, get_user_id_from_token
from datetime import date
from mariadb import IntegrityError

router = APIRouter(prefix="/readings", tags=["Readings"])

@router.get("/", response_model=list[ReadingDb], status_code=status.HTTP_200_OK)
async def get_reading(reading_status: str | None = None ,token: str = Depends(oauth2_scheme)):
    # if status none devuelve todas las lecturas del usuario
    if not status:
        return get_readings_db()
    
    # Query parameter - filrar por status process - finished - desired
    if reading_status not in ["process","finished","desired"]:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail ="invalid status. It must be <process>,<finished>, <desired>"
        )

    return get_readings_by_status(reading_status)

 
    
