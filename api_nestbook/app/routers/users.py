# Tengo que importar todas las clases
from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm

# tengo que importar las clases bassemodel
from app.models import UserBase,UserIn,UserDb,UserLoginIn
from app.auth.auth import create_access_token, Token, verify_password
from app.database import users, insert_user


# APIRouter included in app (FastAPI)
router = APIRouter(prefix="/users", tags=["Users"])


# Signup and create new user.
@router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserIn):
    userDb = get_user_by_username(userIn.username)

    if userDb:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    insert_user(
        UserDb(
            # id=len(users) + 1,
            name=user_in.name,
            username=user_in.username,
            password=user_in.password,
            email=user_in.email,
            phone=user_in.phone,
        )
    )


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
    
    # 2 Buscoo username en la base de datos
    user_found = [user for user in users if user.username == user_login.username]
    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usarme and/or password incorrect",
        )

    #3. Compruebo contraseñas
    user: UserDb = user_found[0]
    if not verify_password(password,user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usarme and/or password incorrect",
        )

    token = create_access_token(
        UserBase(
            username=user.username,
            password=user.password

            )
        )
    return token

# Lo copio del profe medio copiado

# Get users
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

