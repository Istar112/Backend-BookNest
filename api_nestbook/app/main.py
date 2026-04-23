from fastapi import FastAPI

from app.routers import users
from app.routers import books
from app.routers import authors
from app.routers import users,books, readings

# New instance of FastAPI
app = FastAPI(debug=True)

API_V1_PREFIX = "/api/v1"

# Including our router in app
app.include_router(users.router, prefix=API_V1_PREFIX)
app.include_router(books.router, prefix=API_V1_PREFIX)
app.include_router(authors.router, prefix=API_V1_PREFIX)
app.include_router(readings.router, prefix=API_V1_PREFIX)


# Ruta home
@app.get("/")
async def root():
    return {"message": "Welcome to my first FastAPI API"}
