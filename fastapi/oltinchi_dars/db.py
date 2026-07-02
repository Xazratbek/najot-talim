from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

DATABASE_URL = 'postgresql+asyncpg://xazratbek:196712@localhost:5432/oltinchi_dars'

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        yield session
