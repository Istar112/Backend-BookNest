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


# router
router = APIRouter(prefix="/authors", tags=["Authors"])


# Crear un autor
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_author(author_in: AuthorBase, token: str = Depends(oauth2_scheme)):
    existing_author = get_author_by_name(author_in.name_author)#validación
    if existing_author:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Author already exists"
        )
    
    # Se inserta en la bbdd
    author_id = insert_author(
        AuthorDb(
            id=0,
            name_author=author_in.name_author,
            country=author_in.country,
            image=author_in.image
        )
    )

    return {"message": "Author created successfully", "id": author_id}
