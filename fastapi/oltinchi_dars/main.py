from contextlib import asynccontextmanager
from fastapi import FastAPI
from db import engine, Base
import product.models
from product.router import router as product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(product_router)
