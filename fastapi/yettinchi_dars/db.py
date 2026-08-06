import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://xazratbek:196712@localhost:5432/yettinchi_dars",
)

engine = create_async_engine(settings.database_url)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

async def get_db():
    async with SessionLocal() as db:
        yield db
