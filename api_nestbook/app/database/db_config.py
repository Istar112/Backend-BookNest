from app.config import settings

db_config = {
    "host": settings.MARIADB_HOST,
    "port": settings.MARIADB_PORT,
    "user": settings.MARIADB_USER,
    "password": settings.MARIADB_PASSWORD,
    "database": settings.MARIADB_DATABASE,
}