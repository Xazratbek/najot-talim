from fastapi import FastAPI
import auth
from auth_router import router as auth_router

app = FastAPI(title="Blog Site")

app.include_router(auth_router)
