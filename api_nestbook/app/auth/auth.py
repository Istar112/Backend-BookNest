import bcrypt

from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel

from app.models import UserBase

SECRET_KEY = "1234567890"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 7 * 24 * 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def get_hash_password(plain_pw: str) -> str:
    pw_bytes = plain_pw.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password=pw_bytes, salt=salt)
    return hashed_pw.decode("utf-8")


def verify_password(plain_pw, hashed_pw) -> bool:
    plain_pw_bytes = plain_pw.encode("utf-8")
    hashed_pw_bytes = hashed_pw.encode("utf-8")
    return bcrypt.checkpw(password=plain_pw_bytes, hashed_password=hashed_pw_bytes)

# La funcion del profe con UserBase
# def create_access_token(user: UserBase) -> Token:
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
#     to_encode = {"sub": user.username, "exp": expire}
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return Token(access_token=encoded_jwt, token_type="bearer")

# Nueva funcion sin contraseña en el token
def create_access_token(user_id: int, username: str) -> Token:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    to_encode = {
        "sub": username,
        "user_id": user_id, 
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer")



def decode_token(token: str) -> TokenData:
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(username=payload.get("sub"))
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
# Añadido la funcion de obtener el id del usuario registrado
def get_user_id_from_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

