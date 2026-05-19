import mariadb
from app.database.db_config import db_config
import logging
from app.models.author import AuthorDb


def insert_author(author: AuthorDb) -> int:
    try:
        with mariadb.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                sql = "INSERT INTO author (name_author, country, image) VALUES (?,?,?)"
                values = (author.name_author, author.country, author.image)
                cursor.execute(sql, values)
                conn.commit()
                return cursor.lastrowid  # Devuelve el ID del nuevo autor.
    except Exception as e:
        logging.error(f"Error al insertar autor: {e}")
        return 0
    

def get_author_by_name(name_author: str) -> AuthorDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, name_author, country, image FROM author WHERE name_author=?"
            cursor.execute(sql, (name_author,))
            row = cursor.fetchone()

            if row is None:
                return None

            return AuthorDb(
                id=row[0],
                name_author=row[1],
                country=row[2],
                image=row[3],
            )
