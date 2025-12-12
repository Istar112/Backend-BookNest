from fastapi import FastAPI

from app.routers import users
from app.routers import books

# New instance of FastAPI
app = FastAPI(debug=True)

# Including our router in app
app.include_router(users.router)
app.include_router(books.router)


# Ruta home
@app.get("/")
async def root():
    return {"message": "Welcome to my first FastAPI API"}
