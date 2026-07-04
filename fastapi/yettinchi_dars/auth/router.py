from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db import get_db
import auth.crud as crud
import auth.schema as schema
from auth.dependencies import get_current_user
from auth.models import User

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/signup', response_model=schema.MessageResponse, status_code=status.HTTP_201_CREATED)
def signup_router(data: schema.SignupSchema, session: Session = Depends(get_db)):
    return crud.signup(session, data)


@router.post('/login', response_model=schema.TokenResponse)
def login_router(data: schema.LoginSchema, session: Session = Depends(get_db)):
    return crud.login(session, data)


@router.get('/profile', response_model=schema.ProfileSchema)
def profile_router(user: User = Depends(get_current_user)):
    return crud.get_profile(user)


@router.patch('/profile-update', response_model=schema.ProfileSchema)
def profile_update_router(data: schema.ProfileUpdateSchema, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return crud.update_profile(session, data, user)


@router.post('/password-change', response_model=schema.MessageResponse)
def password_change_router(data: schema.PasswordChangeSchema, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return crud.change_password(session, data, user)
