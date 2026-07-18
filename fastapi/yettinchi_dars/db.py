import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://xazratbek:196712@localhost:5432/yettinchi_dars",
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
