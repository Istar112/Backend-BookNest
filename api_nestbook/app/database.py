from app.models import UserDb,BookDb
import mariadb

db_config = {
    "host": "myapidb",
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi",
}


def insert_user(user: UserDb):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "insert into user(name, username,email,phone,password) values (?,?,?,?,?)"
            values = (user.name, user.username, user.email, user.phone, user.password)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid


def get_user_by_username(username: str) -> UserDb | None:
    # TODOterminar esta funcion
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, username, name, password, email, phone FROM user WHERE username=? "
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

def get_book_by_isbn(isbn: str) -> BookDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, isbn, title, category, total_pages, publication_date, purchased FROM book WHERE isbn=?"
            cursor.execute(sql,(isbn,))

            row= cursor.fetchone()
            
            if row is None:
                return None
            
            return BookDb(
                id=row[0],
                isbn=row[1],
                title=row[2],
                category=row[3],
                total_pages=row[4],
                publication_date=row[5],
                purchased=row[6]
            )
            

def insert_book(bookDb:BookDb) -> int | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO book(isbn,title,category,total_pages,publication_date,purchased) values (?,?,?,?,?,?)"
            values = (bookDb.isbn,bookDb.title,bookDb.category,bookDb.total_pages,bookDb.publication_date,bookDb.purchased)
            cursor.execute(sql,values)
            conn.commit()
            return cursor.lastrowid


def get_all_books() -> list[BookDb]:

    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, isbn, title, category, total_pages, publication_date, purchased FROM book"
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
                        purchased=row[6]
                    )
                )
            return books
        


        

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
