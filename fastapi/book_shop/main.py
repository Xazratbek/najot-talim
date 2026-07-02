from fastapi import FastAPI
from book.router import router as book_router
from auth.router import router as auth_router


app = FastAPI()

app.include_router(book_router, prefix='')
app.include_router(auth_router)
