# Tengo que importar todas las clases
from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm

# tengo que importar las clases bassemodel
from app.models import UserBase,UserIn,UserDb,UserLoginIn
from app.auth.auth import create_access_token, Token, verify_password, get_hash_password
from app.database import users, insert_user, get_user_by_username


# APIRouter included in app (FastAPI)
router = APIRouter(prefix="/users", tags=["Users"])


# Signup and create new user.
@router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserIn):
    userDb = get_user_by_username(user_in.username)

    if userDb:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
    
    hashed_password = get_hash_password(user_in.password)

    insert_user(
        UserDb(
            id=len(users) + 1,
            name=user_in.name,
            username=user_in.username,
            password=hashed_password,
            email=user_in.email,
            phone=user_in.phone
        )
    )
    return {"message": "User created successfully"}



# Login and validate
# Depends clase de de FastApi
# form_data es una clase no un diccionario
@router.post("/login/", response_model=Token, status_code=status.HTTP_200_OK)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. Para acceder a username y password?
    username :str | None = form_data.username
    password :str | None = form_data.password

    if username is None or password is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username and/or password incorrect"
        )
    
    # Para memoria
    # user_found = [user for user in users if user.username == form_data.username]
    # 2. Busco el usuario en la base de datos
    user_found = get_user_by_username(username)

    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usernarme and/or password incorrect",
        )

   
    #3. Compruebo contraseñas
    if not verify_password(password,user_found.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usernarme and/or password incorrect",
        )

    token = create_access_token(
        UserBase(
            username=user_found.username,
            password=user_found.password

            )
        )
    return token



    



"""
@router.get(

)
async def get_all_users(token: str = Depends(oauth2_schema)):
    data: TokenData = decode_token(token)

    if data.username not in [u.username for u in users)]:
        raise HTTPException(
            status_code=statu
        )
    
    return [
        UserOut(id=UserDb.id)
    ]

"""

