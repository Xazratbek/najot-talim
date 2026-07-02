from db import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, func


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    hashed_password = Column(String(255))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
