# Tengo que importar todas las clases
from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm

# tengo que importar las clases bassemodel
from app.models import BookBase, BookDb
from app.database import get_book_by_isbn,insert_book

router = APIRouter(prefix="/books", tags=["Books"])

# Create a book
@router.post("/create_book/", status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookBase):
    bookDb = get_book_by_isbn(book_in.isbn)

    if bookDb:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Book already exists"
        )
    
    insert_book(
        BookDb(
            id=0,
            isbn=book_in.isbn,
            title=book_in.title,
            category=book_in.category,
            total_pages=book_in.total_pages,
            publication_date=book_in.publication_date,
            purchased=book_in.purchased
        )
    )
    return {"message": "User created successfully"}    

#@router.get("/get_book")