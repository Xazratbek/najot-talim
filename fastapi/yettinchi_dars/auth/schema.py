from pydantic import BaseModel
from typing import Optional


class SignupSchema(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    password: str


class LoginSchema(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class ProfileSchema(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]

    class Config:
        from_attributes = True


class ProfileUpdateSchema(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None


class PasswordChangeSchema(BaseModel):
    old_password: str
    new_password: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class MessageResponse(BaseModel):
    message: str
