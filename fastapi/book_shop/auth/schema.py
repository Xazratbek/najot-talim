from pydantic import BaseModel


class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str


class LoginSchema(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access: str
    refresh: str


class UserProfileSchema(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str
