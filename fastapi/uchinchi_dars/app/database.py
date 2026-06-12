import os
from pathlib import Path
from collections.abc import AsyncGenerator
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import ssl


def load_dotenv(path: str | Path = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return

    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"\'')
        os.environ.setdefault(key, value)


load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://xazratbek:196712@localhost/mashinalar"
)


def normalize_asyncpg_url(database_url: str) -> tuple[str, dict[str, str]]:
    url = make_url(database_url)
    connect_args: dict[str, object] = {}

    if url.drivername != "postgresql+asyncpg":
        return database_url, connect_args

    query = dict(url.query)
    query.pop("sslmode", None)
    query.pop("ssl", None)

    if url.query != query:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        connect_args["ssl"] = ctx

    return str(url.set(query=query)), connect_args


DATABASE_URL, CONNECT_ARGS = normalize_asyncpg_url(DATABASE_URL)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    connect_args=CONNECT_ARGS,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession,None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
