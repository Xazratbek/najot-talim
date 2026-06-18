from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext
from database import get_db
from models import User
from schemas import (
    UserRegister, UserLogin, TokenResponse,
    UserProfile, MessageResponse
)

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    existing = db.execute(
        select(User).where((User.username == data.username) | (User.email == data.email))
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username yoki email allaqachon mavjud"
        )

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=pwd_context.hash(data.password),
        is_author=data.is_author,
    )
    db.add(user)
    db.commit()
    return MessageResponse(message="Ro'yxatdan o'tish muvaffaqiyatli")


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    user = db.execute(
        select(User).where(User.username == data.username)
    ).scalar_one_or_none()

    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username yoki password noto'g'ri"
        )

    access = authorize.create_access_token(subject=user.id)
    refresh = authorize.create_refresh_token(subject=user.id)
    return TokenResponse(access=access, refresh=refresh)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()
    user_id = authorize.get_jwt_subject()
    access = authorize.create_access_token(subject=user_id)
    refresh = authorize.create_refresh_token(subject=user_id)
    return TokenResponse(access=access, refresh=refresh)


@router.get("/profile", response_model=UserProfile)
def get_profile(authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()

    user = db.execute(
        select(User).where(User.id == user_id)
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foydalanuvchi topilmadi"
        )
    return user
