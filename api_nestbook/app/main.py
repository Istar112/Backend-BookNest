from fastapi import FastAPI

from app.routers import users

# New instance of FastAPI
app = FastAPI(debug=True)

# Including our router in app
app.include_router(users.router)


# Ruta home
@app.get("/")
async def root():
    return {"message": "Welcome to my first FastAPI API"}
