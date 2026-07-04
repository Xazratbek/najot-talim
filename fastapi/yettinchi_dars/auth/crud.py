from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException, status
from auth.models import User, TokenBlacklist
from auth.schema import SignupSchema, LoginSchema, ProfileUpdateSchema, PasswordChangeSchema
from auth.auth_config import create_access_token, create_refresh_token, decode_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def signup(session: Session, data: SignupSchema):
    existing = session.query(User).filter(
        (User.username == data.username) | (User.email == data.email)
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username yoki email allaqachon mavjud"
        )

    user = User(
        username=data.username,
        email=data.email,
        full_name=data.full_name,
        hashed_password=pwd_context.hash(data.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return {'message': "Ro'yxatdan o'tish muvaffaqiyatli"}


def login(session: Session, data: LoginSchema):
    user = session.query(User).filter(User.username == data.username).first()

    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username yoki password noto'g'ri"
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return {'access_token': access_token, 'refresh_token': refresh_token}


def get_profile(user: User):
    return user


def update_profile(session: Session, data: ProfileUpdateSchema, user: User):
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    session.commit()
    session.refresh(user)

    return user


def change_password(session: Session, data: PasswordChangeSchema, user: User):
    if not pwd_context.verify(data.old_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Eski parol noto'g'ri"
        )

    user.hashed_password = pwd_context.hash(data.new_password)
    session.commit()

    return {'message': "Parol muvaffaqiyatli o'zgartirildi"}


def refresh_access_token(refresh_token: str):
    try:
        payload = decode_token(refresh_token)
        user_id = int(payload.get('sub'))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token noto'g'ri yoki eskirgan"
        )

    access_token = create_access_token(user_id)
    return {'access_token': access_token, 'refresh_token': refresh_token}


def logout(session: Session, access_token: str):
    existing = session.query(TokenBlacklist).filter(TokenBlacklist.token == access_token).first()
    if existing:
        return {'message': "Allaqachon chiqib ketgansiz"}

    blacklisted_token = TokenBlacklist(token=access_token)
    session.add(blacklisted_token)
    session.commit()
    return {'message': "Muvaffaqiyatli chiqib ketdingiz"}
