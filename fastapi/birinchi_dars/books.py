from fastapi import APIRouter
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str

router = APIRouter(prefix="/books",tags=["Books"])

@router.get("/")
async def get_book():
    return {"message":"Barcha kitoblar ro'yxati","books":["Kitob 1","Kitob 2"]}

@router.post("/")
async def add_book(book: Book):
    return {"message":"Kitob qo'shildi","book": book}