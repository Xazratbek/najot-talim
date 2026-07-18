from fastapi import FastAPI
from db import engine, Base
import auth.models
from auth.router import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
