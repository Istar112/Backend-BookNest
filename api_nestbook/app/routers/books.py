# Tengo que importar todas las clases
from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm

#lista para libros
from typing import List
# tengo que importar las clases bassemodel
from app.models import BookBase, BookDb
from app.database import (
    insert_book,
    get_all_books,
    get_book_by_isbn,
)


router = APIRouter(prefix="/books", tags=["Books"])

# Create a book
@router.post("/create_book/", status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookBase):
    existing = get_book_by_isbn(book_in.isbn)

    if existing:
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
    return {"message": "Book created successfully"}    

@router.get("/get_books/", response_model=List[BookDb], status_code=status.HTTP_200_OK)
async def get_books():
    try:
        books = get_all_books()
    except MariaDBError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}"
        )
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="get_all_books not implemented in app.database"
        )

    return books

@router.get("/get_book/{isbn}", response_model=BookDb, status_code=status.HTTP_200_OK)
async def get_book_by_isbn_endpoint(isbn: str):
    book = get_book_by_isbn(isbn)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book