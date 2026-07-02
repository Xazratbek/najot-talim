import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-jwt-key-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_token(user_id: int, token_type: str, expires_delta: timedelta) -> str:
    payload = {
        'sub': str(user_id),
        'type': token_type,
        'exp': datetime.now(timezone.utc) + expires_delta,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user_id: int) -> str:
    return create_token(user_id, 'access', timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


def create_refresh_token(user_id: int) -> str:
    return create_token(user_id, 'refresh', timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
