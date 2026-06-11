from fastapi import FastAPI
from books import router as books_router
from students import router as students_router
from tasks import router as tasks_router
from blog import router as blog_router

app = FastAPI()

app.include_router(books_router)
app.include_router(students_router)
app.include_router(tasks_router)
app.include_router(blog_router)