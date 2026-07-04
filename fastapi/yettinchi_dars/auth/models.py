from db import Base
from sqlalchemy import Column, String, Integer, DateTime, func


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    full_name = Column(String(120), nullable=True)
    hashed_password = Column(String(255))
    created_at = Column(DateTime, default=func.now())


class TokenBlacklist(Base):
    __tablename__ = 'token_blacklist'

    id = Column(Integer, primary_key=True)
    token = Column(String(500), unique=True)
    blacklisted_at = Column(DateTime, default=func.now())
