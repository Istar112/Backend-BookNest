from app.database.db_config import db_config
import mariadb
import logging
from app.models.book import BookDb

def get_book_by_isbn(isbn: str) -> BookDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, isbn, title, category, total_pages, publication_date, purchased, cover_image FROM book WHERE isbn=?"
            print(f"[DEBUG] Executing get_book_by_isbn with isbn={repr(isbn)}")
            cursor.execute(sql, (isbn,))
            row = cursor.fetchone()
            print(f"[DEBUG] get_book_by_isbn result row={row!r}")
            if row is None:
                return None

            return BookDb(
                id=row[0],
                isbn=row[1],
                title=row[2],
                category=row[3],
                total_pages=row[4],
                publication_date=row[5],
                purchased=row[6],
                cover_image =row[7],
            )


def get_book_by_title_db(title: str) -> list[BookDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, isbn, title, category, total_pages, publication_date, purchased, cover_image FROM book WHERE title LIKE ?"
            print(f"[DEBUG] Executing get_book_by_title with title={repr(title)}")
            cursor.execute(sql, (f"%{title}%",))
            rows = cursor.fetchall()
            logging.debug(f"[DEBUG] get_book_by_title result rows={rows!r}")
            books = []      
            for row in rows:
                logging.debug(f"FILA: {row[2]}")
                book = BookDb(
                    id=row[0],
                    isbn=row[1],
                    title=row[2],
                    category=row[3],
                    total_pages=row[4],
                    publication_date=row[5],
                    purchased=row[6],
                    cover_image = row[7]
                )
                books.append(book)
            return books
        
      
def get_book_by_id_db(id:int) -> BookDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, isbn, title, category, total_pages, publication_date, purchased, cover_image FROM book WHERE id=?"
            print(f"[DEBUG] Executing get_book_by_id_db with id={repr(id)}")
            cursor.execute(sql,(id,))
            row = cursor.fetchone()
            print(f"[DEBUG] get_book_by_id_db result row={row!r}")
            if row is None:
                return None
            
            return BookDb(
                id=row[0],
                isbn=row[1],
                title=row[2],
                category=row[3],
                total_pages=row[4],
                publication_date=row[5],
                purchased=row[6],
                cover_image=row[7]
            )
    

def delete_book_by_id(book_id: int) -> bool:
    try:
        with mariadb.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM book WHERE id = ?"
                cursor.execute(sql, (book_id,))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logging.error(f"Error deleting user with ID {book_id}: {e}")
        return False
    

def update_book_by_id(book_id: int, updated_data: dict) -> bool:
    try:
        with mariadb.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                fields = [f"{key} = ?" for key in updated_data.keys()]
                sql = f"UPDATE book SET {', '.join(fields)} WHERE id = ?"
                values = list(updated_data.values()) + [book_id]
                logging.debug(f"Ejecutando SQL: {sql} con valores: {values}")
                cursor.execute(sql, values)
                conn.commit()
                return cursor.rowcount > 0           
    except Exception as e:
        logging.error(f"Error al actualizar el libro con ID {book_id}: {e}")
        return False
    
            
def insert_book(bookDb: BookDb) -> int | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO book(isbn, title, category, total_pages, publication_date, purchased, cover_image) VALUES (?,?,?,?,?,?,?)"
            values = (bookDb.isbn, bookDb.title, bookDb.category, bookDb.total_pages, bookDb.publication_date, bookDb.purchased, bookDb.cover_image)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid


def get_all_books() -> list[BookDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, isbn, title, category, total_pages, publication_date, purchased, cover_image FROM book"
            cursor.execute(sql)
            rows = cursor.fetchall()

            books: list[BookDb] = []
            for row in rows:
                books.append(
                    BookDb(
                        id=row[0],
                        isbn=row[1],
                        title=row[2],
                        category=row[3],
                        total_pages=row[4],
                        publication_date=row[5],
                        purchased=row[6],
                        cover_image=row[7]
                    )
                )
            return books