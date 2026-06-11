from fastapi import APIRouter, Depends, HTTPException
from crud import list_books, create_book, read_book, update_book, patch_book
from schemas import BookCreate, BookUpdate, BookResponse
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/library", tags=["Kutubxona tizimi CRUD"])

@router.get("/", response_model=list[BookResponse])
async def get_all_book(db: Session = Depends(get_db)):
    return list_books(db=db)

@router.post("/", response_model=BookResponse)
async def add_book(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(book=book, db=db)

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = read_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookResponse)
async def replace_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    updated = update_book(db, book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.patch("/{book_id}", response_model=BookResponse)
async def modify_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    updated = patch_book(db, book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated