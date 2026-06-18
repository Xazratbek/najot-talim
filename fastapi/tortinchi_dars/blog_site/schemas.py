from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    is_author: bool = False


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access: str
    refresh: str


class UserProfile(BaseModel):
    id: int
    username: str
    email: str
    is_author: bool

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str
