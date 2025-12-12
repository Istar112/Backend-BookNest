from app.models import UserDb
import mariadb

db_config = {
    "host": "myapidb",
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi",
}


# Tengo que ajustar a los valores que tenemos nosotros
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


# select_query = "SELECT id, name, email FROM users WHERE name LIKE ?"
# cursor.execute(select_query, ("%Alice%",)) # Note the comma for single parameter tuple

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
