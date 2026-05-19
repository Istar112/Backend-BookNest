from app.models.reading import ReadingDb, Process, Finished, ProcessDb, FinishedDb
from app.database.db_config import db_config
import mariadb
import logging
from datetime import date 

def insert_status() -> int:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO status () VALUES ()"
            cursor.execute(sql)
            conn.commit()
            new_id = cursor.lastrowid
    return new_id


def insert_process(status_id:int , process: ProcessDb ) -> None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO process (id, num_pag, date_start) VALUES (?,?,?)"
            values = (status_id,process.num_pag, process.date_start)
            cursor.execute(sql,values)
            conn.commit()


def insert_finished(status_id:int , finished: FinishedDb) -> None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO finished (id, finish_date, rating) VALUES (?,?,?)"
            values = (status_id, finished.finish_date, finished.rating)
            cursor.execute(sql,values)
            conn.commit()


def insert_reading(reading : ReadingDb) -> None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO reading (id_user,id_book, id_status, reading_status) VALUES (?,?,?,?)"
            values = (reading.id_user, reading.id_book, reading.id_status, reading.reading_status)
            cursor.execute(sql,values)
            conn.commit()


def get_readings_db() -> list[ReadingDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, id_user, id_book, reading_status, id_status FROM reading"
            cursor.execute(sql)
            rows = cursor.fetchall()

            readings: list[ReadingDb] = []
            for row in rows:
                readings.append(
                    ReadingDb(
                        id=row[0],
                        id_user=row[1],
                        id_book=row[2],
                        reading_status= row[3],
                        id_status=row[4]
                    )
                )
            return readings


def get_readings_by_status(status:str) -> list[ReadingDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, id_user, id_book, reading_status, id_status FROM reading WHERE reading_status=?"
            cursor.execute(sql,(status.lower(),))
            rows = cursor.fetchall()

            readings: list[ReadingDb] = []
            for row in rows:
                readings.append(
                    ReadingDb(
                        id=row[0],
                        id_user=row[1],
                        id_book=row[2],
                        reading_status= row[3],
                        id_status=row[4]
                    )
                )
            return readings


def get_reading_by_user_and_book(user_id: int, book_id: int) -> ReadingDb | None:
    try:
        with mariadb.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                sql = "SELECT id, id_user, id_book, reading_status, id_status FROM reading WHERE id_user=? AND id_book=?"
                cursor.execute(sql, (user_id, book_id))
                row = cursor.fetchone()
                if row:
                    return ReadingDb(id=row[0], id_user=row[1], id_book=row[2], reading_status=row[3], id_status=row[4])
                return None
    except mariadb.Error as e:
        logging.error(f"Error getting reading: {e}")
        return None


def add_finished(readingDb: ReadingDb, finished: FinishedDb) -> None:
    id_status = insert_status()
    readingDb.id_status = id_status
    insert_finished(id_status, finished)
    insert_reading(readingDb)


def add_process(readingDb: ReadingDb, process: ProcessDb) -> None:
    id_status = insert_status()
    readingDb.id_status = id_status
    insert_process(id_status, process)
    insert_reading(readingDb)


def update_finished(finished: FinishedDb) -> bool:
    if not (finished.finish_date or finished.rating):
        return False
    try:
        with mariadb.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE finished SET finish_date = ?, rating = ? WHERE id = ?",
                    (finished.finish_date, finished.rating, finished.id)
                )
                conn.commit()
                return cursor.rowcount > 0
    except mariadb.Error as e:
        logging.error(f"Error updating finished: {e}")
        return False


def update_process(process: ProcessDb) -> bool:
    if process.num_pag is None and process.date_start is None:
        return False
    try:
        with mariadb.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE process SET num_pag = ?, date_start = ? WHERE id = ?",
                    (process.num_pag, process.date_start, process.id)
                )
                conn.commit()
                return cursor.rowcount > 0
    except mariadb.Error as e:
        logging.error(f"Error updating process: {e}")
        return False
 
      
def change_reading_status_to_finished(reading_id: int, finished: FinishedDb) -> bool:
    try:
        with mariadb.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_status, reading_status FROM reading WHERE id = ?",(reading_id,),)
                row = cursor.fetchone()

                if not row:
                    return False
                
                old_status_id = row[0]
                old_status_type = row[1]

                if old_status_type == "finished":
                    finished.id = old_status_id  
                    return update_finished(finished)
                
                if old_status_type == "process":
                    cursor.execute("DELETE FROM process WHERE id = ?", (old_status_id,))

                cursor.execute("INSERT INTO finished (id, finish_date, rating) VALUES (?, ?, ?)",(old_status_id, finished.finish_date, finished.rating))
                cursor.execute( "UPDATE reading SET reading_status=? WHERE id=?",("finished", reading_id))
                conn.commit()
                return True
    except mariadb.Error as e:
        logging.error(f"Error changing status: {e}")
        conn.rollback()
        return False


def change_reading_status_to_process(reading_id: int, process: ProcessDb) -> bool:
    try:
        with mariadb.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute( "SELECT id_status, reading_status FROM reading WHERE id = ?",(reading_id,),)
                row = cursor.fetchone()

                if not row:
                    return False
                
                old_status_id = row[0]
                old_status_type = row[1]

                if old_status_type == "process":
                    process.id = old_status_id
                    return update_process(process) 
                               
                if old_status_type == "finished":
                    cursor.execute("DELETE FROM finished WHERE id = ?", (old_status_id,))

                sql = "INSERT INTO process (id, num_pag, date_start) VALUES (?, ?, ?)"
                values = (old_status_id, process.num_pag, process.date_start)
                cursor.execute(sql, values)

                sql_update = "UPDATE reading SET reading_status=? WHERE id=?"
                cursor.execute(sql_update, ("process", reading_id))

                conn.commit()
                return True
    except mariadb.Error as e:
        logging.error(f"Error changing status: {e}")
        conn.rollback()
        return False


def get_reading_by_id_db(reading_id: int) -> ReadingDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, id_user, id_book, reading_status, id_status FROM reading WHERE id=?"
            cursor.execute(sql, (reading_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return ReadingDb(
                id=row[0],
                id_user=row[1],
                id_book=row[2],
                reading_status=row[3],
                id_status=row[4]
            )


def get_readings_by_user(user_id: int, status: str | None = None) -> list[ReadingDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            if status:
                sql = "SELECT id, id_user, id_book, reading_status, id_status FROM reading WHERE id_user=? AND reading_status=?"
                cursor.execute(sql, (user_id, status))
            else:
                sql = "SELECT id, id_user, id_book, reading_status, id_status FROM reading WHERE id_user=?"
                cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()
            readings: list[ReadingDb] = []
            for row in rows:
                readings.append(
                    ReadingDb(
                        id=row[0],
                        id_user=row[1],
                        id_book=row[2],
                        reading_status=row[3],
                        id_status=row[4]
                    )
                )
            return readings