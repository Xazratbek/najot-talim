from typing import Optional
from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None

class BookResponse(BaseModel):
    id: int
    title: str
    author: str

    class Config:
        orm_mode = True