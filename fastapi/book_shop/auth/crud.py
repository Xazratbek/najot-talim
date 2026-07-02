from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException, status
from auth.models import User
from auth.schema import RegisterSchema, LoginSchema
from auth.auth_config import create_access_token, create_refresh_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register(session: Session, data: RegisterSchema):
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

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    return {'access': access, 'refresh': refresh}
