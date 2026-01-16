from app.models import *
import mariadb
import logging
from datetime import date

logging.basicConfig(level=logging.DEBUG)

# Configuraciones de la conexion de mariaDb
db_config = {
    "host": "myapidb",
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi",
}

# Insertar un usuario
def insert_user(user: UserDb):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO user(name, username, email, phone, password) VALUES (?,?,?,?,?)"
            values = (user.name, user.username, user.email, user.phone, user.password)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid

# Obtener el usuario por el nombre
def get_user_by_username(username: str) -> UserDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, username, name, password, email, phone FROM user WHERE username=?"
            cursor.execute(sql, (username,))

            row = cursor.fetchone()

            if row is None:
                return None

            return UserDb(
                id=row[0],
                username=row[1],
                name=row[2],
                password=row[3],
                email=row[4],
                phone=row[5],
            )
        

# Obtener el usuario por el id
def get_user_by_id(id: int) -> UserDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, username, name, password, email, phone FROM user WHERE id=?"
            cursor.execute(sql, (id,))

            row = cursor.fetchone()

            if row is None:
                return None

            return UserDb(
                id=row[0],
                username=row[1],
                name=row[2],
                password=row[3],
                email=row[4],
                phone=row[5],
            )
        

# Modificar un usuario por id
def update_user_by_id(user_id: int, user_data: UserUpdate) -> bool:

    try:
        with mariadb.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                # lista hecha para poder ir modificando los campos
                fields = []
                values = []

                if user_data.name:
                    fields.append("name = ?")
                    values.append(user_data.name)
                if user_data.username:
                    fields.append("username = ?")
                    values.append(user_data.username)
                if user_data.email:
                    fields.append("email = ?")
                    values.append(user_data.email)
                if user_data.phone:
                    fields.append("phone = ?")
                    values.append(user_data.phone)
                if user_data.password:  # actualizar contraseña
                    fields.append("password = ?")
                    values.append(user_data.password)

                # Si no hay cambios, salir
                if not fields:
                    logging.debug("There are no fields to update.")
                    return False

                # Construir la consulta SQL
                query = f"UPDATE user SET {', '.join(fields)} WHERE id = ?"
                values.append(user_id)  # Agregar el ID al final de los valores

                # Ejecutar la consulta
                logging.debug(f"Running query: {query} with values: {values}")
                cursor.execute(query, tuple(values))
                conn.commit()

                # devuelve TRUE si han habido cambios y FALSE si no ha encontrado al usuario
                return cursor.rowcount > 0
    except Exception as e:
        logging.error(f"Error updating user with ID {user_id}: {e}")
        return False
    

# Buscar un libro por el isbn
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

# Buscar un libro por el título
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
        
# Obtener un libro por su id        
def get_book_by_id_db(id:int) -> BookDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, isbn, title, category, total_pages, publication_date, purchased, cover_image FROM book WHERE id=?"
            print(f"[DEBUG] Executing get_book_by_id_db with id={repr(id)}")
            cursor.execute(sql,(id,))
            row = cursor.fetchone()
            print(f"[DEBUG] get_book_by_id_db result row={row!r}")
            if row is None:
                return "Book doesn't exists"
            
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

            
# Insertar un libro
def insert_book(bookDb: BookDb) -> int | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO book(isbn, title, category, total_pages, publication_date, purchased, cover_image) VALUES (?,?,?,?,?,?,?)"
            values = (bookDb.isbn, bookDb.title, bookDb.category, bookDb.total_pages, bookDb.publication_date, bookDb.purchased, bookDb.cover_image)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid

# Obtener todos los libros 
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

# Insertar un estado
def insert_status() -> int:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO status () VALUES ()"
            cursor.execute(sql)
            conn.commit()
            new_id = cursor.lastrowid
    return new_id

# Insertar en un estado en proceso
def insert_process(status_id:int , process: Process ) -> None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO process (id, num_pag, date_start) VALUES (?,?,?)"
            values = (status_id,process.num_pag, process.date_start)
            cursor.execute(sql,values)
            conn.commit()

# Insertar un estado en terminado
def insert_finished(status_id:int , finished: Finished) -> None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO finished (id, finish_date, rating) VALUES (?,?,?)"
            values = (status_id, finished.finish_date, finished.rating)
            cursor.execute(sql,values)
            conn.commit()

# Insertar un estado en deseado
def insert_desired(status_id: int , desired: Desired) -> None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO desired (id, comment) VALUES (?,?)"
            value = (status_id, desired.comment)
            cursor.execute(sql,value)
            conn.commit()

# Insertar una lectura -Todos los datos relacionados-
def insert_reading(reading : ReadingDb) -> None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO reading (id_user,id_book, id_status, reading_status) VALUES (?,?,?,?)"
            values = (reading.id_user, reading.id_book, reading.id_status, reading.reading_status)
            cursor.execute(sql,values)
            conn.commit()

# id: int
# id_user:int
# id_book: int
# id_status: int
    

# En memoria
users: list[UserDb] = [
    UserDb(
        id=1,
        name="Alice",
        email="alice@gmail.com",
        phone="686868",
        username="alice",
        password="$2b$12$DNz6CV3.zXT.jQ49BGM9W.k/lvaem13d06fGpi6q6TPH8hl/D/c6K",
    ),
    UserDb(
        id=2,
        name="Bob",
        email="bob@gmail.com",
        phone="858585",
        username="bob",
        password="$2b$12$wP/ln00XeTNBXMfCVm8yZeYhjK6JqozucMMOLzGsSfdT9bYwmYpeW",
    ),
]