# imports
from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from app.models.author import AuthorBase, AuthorDb
from app.database.author import insert_author, get_author_by_name   
from app.auth.auth import TokenData, get_current_user
from datetime import date

router = APIRouter(prefix="/authors", tags=["Authors"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_author(author_in: AuthorBase, token: TokenData = Depends(get_current_user)):
    existing_author = get_author_by_name(author_in.name_author)
    if existing_author:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Author already exists"
        )
    
    author_id = insert_author(
        AuthorDb(
            id=0,
            name_author=author_in.name_author,
            country=author_in.country,
            image=author_in.image
        )
    )

    return {"message": "Author created successfully", "id": author_id}