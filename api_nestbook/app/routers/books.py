from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from app.models.book import BookBase, BookDb, BookUpdate
from app.models.reading import FinishedDb, Process, Finished, ProcessDb, ReadingDb, StatusUpdateProcess, StatusUpdateFinished
from app.database.book import (get_book_by_isbn,get_all_books, get_book_by_title_db, get_book_by_id_db, delete_book_by_id, update_book_by_id, insert_book)
from app.database.reading import change_reading_status_to_process, insert_status, insert_process, insert_finished,insert_reading,get_reading_by_user_and_book,update_finished, change_reading_status_to_finished
from app.auth.auth import TokenData, get_current_user
from datetime import date
from mariadb import IntegrityError, Error as MariaDBError

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookBase, token: TokenData = Depends(get_current_user)):
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


@router.get("/{isbn}/", response_model=BookDb, status_code=status.HTTP_200_OK)
async def get_book_by_isbn_endpoint(isbn: str,token: TokenData = Depends(get_current_user)):
    book = get_book_by_isbn(isbn)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.get("/", response_model=List[BookDb], status_code=status.HTTP_200_OK)
async def get_book_by_title(title: str | None = None,token: TokenData = Depends(get_current_user)):
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
    
    books = get_book_by_title_db(title)
    return books


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_book(id: int, book_update: BookUpdate, token: TokenData = Depends(get_current_user)):
    book = get_book_by_id_db(id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {id} does not exist",
        )
    
    updated_book_data = book_update.dict(exclude_unset=True)

    updated = update_book_by_id(id, updated_book_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update book.",
        )

    return {
        "message": "Book updated successfully",
        "updated_fields": updated_book_data
    }


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_book(id: int, token: TokenData = Depends(get_current_user)):
    book = get_book_by_id_db(id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {id} does not exist",
        )

    deleted = delete_book_by_id(id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete book.",
        )

    return {"message": "Book deleted successfully"}


@router.post("/{id}/status/finished",status_code = status.HTTP_200_OK)
async def add_status_finished_to_book (id: int,status_in: StatusUpdateFinished,token: TokenData = Depends(get_current_user) ):
    book: BookDb = get_book_by_id_db(id)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    new_status_id = insert_status()

    status_str = "finished"
    in_finished = Finished(
            id = new_status_id,
            finish_date= status_in.finish_date,
            rating= status_in.rating
        )
    insert_finished(new_status_id,in_finished)    
    
    try:
        insert_reading(
            ReadingDb(
                id_user=token.user_id,
                id_book=id,
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


@router.post("/{id}/status/process",status_code = status.HTTP_200_OK)
async def add_status_process_to_book (id: int,status_in: StatusUpdateProcess,token: TokenData = Depends(get_current_user) ):
    book: BookDb = get_book_by_id_db(id)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    new_status_id = insert_status()

    status_str = "process"

    in_process = Process(
            id = new_status_id,
            num_pag= status_in.num_pag,
            date_start = status_in.date_start
        )
    
    insert_process(new_status_id,in_process)    
    
    try:
        insert_reading(
            ReadingDb(
                id_user=token.user_id,
                id_book=id,
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


@router.put("/{id}/status/finished", status_code=status.HTTP_200_OK)
async def update_status_finished(id: int, status_in: StatusUpdateFinished, token: TokenData = Depends(get_current_user)):
    reading = get_reading_by_user_and_book(token.user_id, id)
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reading for book ID {id} does not exist for the user",
        )
    
    change_reading_status_to_finished(
        reading_id=reading.id,
        finished=FinishedDb(
            finish_date=status_in.finish_date,
            rating=status_in.rating
        )
    )
    return {"message": "Reading status updated to finished successfully"}    


@router.put("/{id}/status/process", status_code=status.HTTP_200_OK)
async def update_status_to_process(id: int, status_in: StatusUpdateProcess, token: TokenData = Depends(get_current_user)):
    reading = get_reading_by_user_and_book(token.user_id, id)
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reading for book ID {id} does not exist for the user",
        )
    
    change_reading_status_to_process(
        reading_id=reading.id,
        process=ProcessDb(
            num_pag=status_in.num_pag,
            date_start=status_in.date_start
        )
    )
    return {"message": "Reading status updated to process successfully"}  