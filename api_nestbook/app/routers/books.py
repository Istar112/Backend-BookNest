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
router = APIRouter(prefix="/books", tags=["Books"])


# Create a book
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookBase, token: str = Depends(oauth2_scheme)):
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
            purchased=book_in.purchased,
            cover_image=book_in.cover_image
        )
    )
    return {"message": "Book created successfully"}    

# Busca un libro por su isbn
@router.get("/{isbn}/", response_model=BookDb, status_code=status.HTTP_200_OK)
async def get_book_by_isbn_endpoint(isbn: str,token: str = Depends(oauth2_scheme)):
    book = get_book_by_isbn(isbn)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

# busca todos los libros si esta vacio o por titulo(Query parameter)
@router.get("/", response_model=List[BookDb], status_code=status.HTTP_200_OK)
async def get_book_by_title(title: str | None = None,token: str = Depends(oauth2_scheme)):
    if not title or not title.strip():
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
    
    # Query parameter
    books = get_book_by_title_db(title)
    return books

# Le asigno un estado a un libro (finished, process o desired)
@router.post("/{idBook}/status",status_code = status.HTTP_200_OK)
async def add_status_to_book (
    idBook: int,
    status_in: StatusUpdate ,
    token: str = Depends(oauth2_scheme) 
):
    book: BookDb = get_book_by_id_db(idBook)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    new_status_id = insert_status()

    status_str = status_in.status_str

    if status_str == "process":
        in_process = Process(
            id = new_status_id,
            num_pag= 0,
            date_start = date.today()
        )
        insert_process(new_status_id,in_process)    
    elif status_str == "finished":
        finished = Finished(
            id = new_status_id,
            finish_date = date.today(),
            rating = None
        )
        insert_finished(new_status_id, finished)
    elif status_str == "desired":
        desired = Desired(
            id = new_status_id,
            comment = None
        )
        insert_desired(new_status_id,desired)
    else:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail= "Invalid status. It must be [process, finished, desired]"
        )
    
    id_user = get_user_id_from_token(token)
    
    try:
        insert_reading(
            ReadingDb(
                id_user=id_user,
                id_book=idBook,
                id_status=new_status_id,
                reading_status=status_str
            )
        )
    except IntegrityError as e:
        if "c_user_book" in str(e):
            raise HTTPException(
                status_code=400,
                detail="This book is already in the user's reading list"
            )
        
    return {"message": "Status added successfully"}   


    
