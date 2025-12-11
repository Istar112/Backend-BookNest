from app.models import UserDb
import mariadb

db_config = {
    "host": "myapidb",
    "port": 3606,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi"
}


# Tengo que ajustar a los valores que tenemos nosotros
def insert_user(user: UserDb):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "insert into userts(name,username,password) values (?,?,?)"
            values = (user.name, user.username,user.password)
            cursor = execute(sql, values)
            return cursor.lastrowid


def get_user_by_username(username: str) -> UserDb | None:
    # TODOterminar esta funcion
    return None



# Hay que adaptarlo despues 
users: list[UserDb] = [
    UserDb(
        id=1,
        name="Alice",
        username="alice",
        password="$2b$12$DNz6CV3.zXT.jQ49BGM9W.k/lvaem13d06fGpi6q6TPH8hl/D/c6K"
    ),
    UserDb(
        id=2,
        name="Bob",
        username="bob",
        password="$2b$12$wP/ln00XeTNBXMfCVm8yZeYhjK6JqozucMMOLzGsSfdT9bYwmYpeW"
    )
]
