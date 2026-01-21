from fastapi import FastAPI

from app.routers import users,books, readings

# New instance of FastAPI
app = FastAPI(debug=True)

# Including our router in app
app.include_router(users.router)
app.include_router(books.router)
app.include_router(readings.router)


# Ruta home
@app.get("/")
async def root():
    return {"message": "Welcome to my first FastAPI API"}
