# imports
from fastapi import APIRouter, status, HTTPException, Depends
from typing import List, Optional
from app.models.reading import ReadingBase, ReadingDb, Finished, Process,StatusDb
from app.database.db_config import db_config
from app.database.reading import get_readings_by_user, get_reading_by_id_db, insert_process, insert_reading, update_finished, insert_finished
from app.auth.auth import TokenData, get_current_user
from datetime import date
import mariadb

router = APIRouter(prefix="/readings", tags=["Readings"])

@router.get("/", response_model=list[ReadingDb], status_code=status.HTTP_200_OK)
async def get_reading(
    reading_status: str | None = None,
    token: TokenData = Depends(get_current_user),
):
    if not reading_status:
        return get_readings_by_user(token.user_id)
    if reading_status not in ["process", "finished"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid status. It must be <process>, <finished>",
        )
    return get_readings_by_user(token.user_id, reading_status)


