import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from db import get_db
import auth.crud as crud
import auth.schema as schema
from auth.dependencies import get_current_user, bearer_scheme
from auth.auth_config import decode_token, create_access_token, create_refresh_token
from auth.models import User

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register', response_model=schema.MessageResponse, status_code=status.HTTP_201_CREATED)
def register_router(data: schema.RegisterSchema, session: Session = Depends(get_db)):
    return crud.register(session, data)


@router.post('/login', response_model=schema.TokenResponse)
def login_router(data: schema.LoginSchema, session: Session = Depends(get_db)):
    return crud.login(session, data)


@router.post('/refresh', response_model=schema.TokenResponse)
def refresh_router(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        payload = decode_token(credentials.credentials)
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token noto'g'ri yoki muddati tugagan")

    if payload.get('type') != 'refresh':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Refresh token kerak')

    user_id = int(payload['sub'])
    access = create_access_token(user_id)
    refresh = create_refresh_token(user_id)

    return {'access': access, 'refresh': refresh}


@router.get('/profile', response_model=schema.UserProfileSchema)
def profile_router(user: User = Depends(get_current_user)):
    return user
