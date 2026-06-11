from fastapi import FastAPI
from database import engine
from models import Book
from routers import router as book_router

app = FastAPI()
app.include_router(book_router)
Book.metadata.create_all(bind=engine)