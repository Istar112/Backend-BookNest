from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserIn, UserDb, UserOut, UserUpdate, UserStreakOut, UserStreakUpdate
from app.models.token import Token, TokenData, RefreshTokenRequest
from app.schemas.profile import ProfileResponse, ProfileUpdateRequest
from app.auth.auth import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    verify_password,
    get_hash_password
)
from app.database.user import (
    insert_user,
    get_user_by_username,
    get_user_by_id,
    update_user_by_id,
    delete_user_by_id,
    update_user_streak
)

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
            id=0,
            name=user_in.name,
            username=user_in.username,
            password=hashed_password,
            email=user_in.email,
            phone=user_in.phone,
            streak_days=0,
            last_reading_date=None
        )
    )
    return {"message": "User created successfully"}


@router.post("/login/", response_model=Token, status_code=status.HTTP_200_OK)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    username: str | None = form_data.username
    password: str | None = form_data.password

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

    if not verify_password(password, user_found.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username and/or password incorrect",
        )

    access_token = create_access_token(
        user_id=user_found.id,
        username=user_found.username
    )
    refresh_token = create_refresh_token(
        user_id=user_found.id,
        username=user_found.username
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh/", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh_user_token(body: RefreshTokenRequest):
    token_data = decode_token(body.refresh_token)

    if token_data.token_type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    if token_data.user_id is None or token_data.username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user = get_user_by_id(token_data.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    access_token = create_access_token(
        user_id=user.id,
        username=user.username
    )
    refresh_token = create_refresh_token(
        user_id=user.id,
        username=user.username
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_user(id: int, user_update: UserUpdate, token: TokenData = Depends(get_current_user)):
    user = get_user_by_id(id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} does not exist",
        )

    if user_update.password is not None:
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


@router.get("/me/", response_model=UserOut, status_code=status.HTTP_200_OK)
async def read_current_user(token: TokenData = Depends(get_current_user)):
    user = get_user_by_id(token.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserOut(
        name=user.name,
        username=user.username,
        email=user.email,
        phone=user.phone
    )


@router.put("/me/", response_model=ProfileResponse, status_code=status.HTTP_200_OK)
async def update_current_user_profile(
    profile_update: ProfileUpdateRequest,
    token: TokenData = Depends(get_current_user)
):
    user = get_user_by_id(token.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    existing_user = get_user_by_username(profile_update.username)
    if existing_user and existing_user.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    user_update = UserUpdate(
        username=profile_update.username,
        password=get_hash_password(profile_update.new_password) if profile_update.new_password else None
    )

    updated = update_user_by_id(user.id, user_update)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update profile.",
        )

    updated_user = get_user_by_id(user.id)

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found after update",
        )

    return ProfileResponse(username=updated_user.username)


@router.get("/streak/", response_model=UserStreakOut, status_code=status.HTTP_200_OK)
async def read_user_streak(token: TokenData = Depends(get_current_user)):
    user = get_user_by_id(token.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserStreakOut(
        streakDays=user.streak_days,
        lastReadingDate=user.last_reading_date
    )


@router.put("/{id}/streak", status_code=status.HTTP_200_OK)
async def modify_user_streak(id: int, streak_update: UserStreakUpdate):
    user = get_user_by_id(id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} does not exist",
        )

    updated = update_user_streak(id, streak_update.streak_days)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user streak.",
        )

    return {"message": "User streak updated successfully"}