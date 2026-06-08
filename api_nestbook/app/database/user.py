from app.database.db_config import db_config
import mariadb
import logging
from app.models.user import UserDb, UserUpdate


def insert_user(user: UserDb):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO user(name, username, email, phone, password, streak_days, last_reading_date) VALUES (?,?,?,?,?,?,?)"
            values = (user.name, user.username, user.email, user.phone, user.password, user.streak_days, user.last_reading_date)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid


def get_user_by_username(username: str) -> UserDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, username, name, password, email, phone, streak_days, last_reading_date FROM user WHERE username=?"
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
                streak_days=row[6],
                last_reading_date=str(row[7]) if row[7] else None
            )


def get_user_by_id(id: int) -> UserDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, username, name, password, email, phone, streak_days, last_reading_date FROM user WHERE id=?"
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
                streak_days=row[6],
                last_reading_date=str(row[7]) if row[7] else None
            )


def update_user_by_id(user_id: int, user_data: UserUpdate) -> bool:
    try:
        with mariadb.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                fields = []
                values = []

                if user_data.name is not None:
                    fields.append("name = ?")
                    values.append(user_data.name)

                if user_data.username is not None:
                    fields.append("username = ?")
                    values.append(user_data.username)

                if user_data.email is not None:
                    fields.append("email = ?")
                    values.append(user_data.email)

                if user_data.phone is not None:
                    fields.append("phone = ?")
                    values.append(user_data.phone)

                if user_data.password is not None:
                    fields.append("password = ?")
                    values.append(user_data.password)

                if user_data.streak_days is not None:
                    fields.append("streak_days = ?")
                    values.append(user_data.streak_days)

                if user_data.last_reading_date is not None:
                    fields.append("last_reading_date = ?")
                    values.append(user_data.last_reading_date)

                if not fields:
                    logging.debug("There are no fields to update.")
                    return False

                query = f"UPDATE user SET {', '.join(fields)} WHERE id = ?"
                values.append(user_id)

                logging.debug(f"Running query: {query} with values: {values}")
                cursor.execute(query, tuple(values))
                conn.commit()

                return cursor.rowcount > 0
    except Exception as e:
        logging.error(f"Error updating user with ID {user_id}: {e}")
        return False


def delete_user_by_id(user_id: int) -> bool:
    try:
        with mariadb.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM user WHERE id = ?"
                cursor.execute(sql, (user_id,))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logging.error(f"Error deleting user with ID {user_id}: {e}")
        return False


def update_user_streak(user_id: int, streak_days: int) -> bool:
    try:
        with mariadb.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                sql = "UPDATE user SET streak_days = ? WHERE id = ?"
                cursor.execute(sql, (streak_days, user_id))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logging.error(f"Error updating streak for user ID {user_id}: {e}")
        return False