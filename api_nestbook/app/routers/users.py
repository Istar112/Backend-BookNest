from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserBase,UserIn,UserDb,UserLoginIn,UserUpdate
from app.auth.auth import TokenData, create_access_token, Token, get_current_user, verify_password, get_hash_password
from app.database.user import insert_user, get_user_by_username, get_user_by_id, update_user_by_id, delete_user_by_id

router = APIRouter(prefix="/users", tags=["Users"])

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
            id=0, # ignored
            name=user_in.name,
            username=user_in.username,
            password=hashed_password,
            email=user_in.email,
            phone=user_in.phone
        )
    )
    return {"message": "User created successfully"}


@router.post("/login/", response_model=Token, status_code=status.HTTP_200_OK)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
   
    username :str | None = form_data.username
    password :str | None = form_data.password

    if username is None or password is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username and/or password incorrect"
        )
    
    user_found = get_user_by_username(username)

    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username and/or password incorrect",
        )

    if not verify_password(password,user_found.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username and/or password incorrect",
        )
    
    token = create_access_token(user_id=user_found.id,username=user_found.username)
    return token


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_user(id: int, user_update: UserUpdate, token: TokenData = Depends(get_current_user)):

    user = get_user_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} does not exist",
        )

    if user_update.password:
        user_update.password = get_hash_password(user_update.password)

    updated = update_user_by_id(id, user_update)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user.",
        )
    
    return {"message": "User updated successfully"}


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id: int, token: TokenData = Depends(get_current_user)):

    user = get_user_by_id(id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} does not exist",
        )

    deleted = delete_user_by_id(id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete user.",
        )

    return {"message": "User deleted successfully"}