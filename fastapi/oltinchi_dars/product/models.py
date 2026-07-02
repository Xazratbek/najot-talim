from db import Base
from sqlalchemy import Column, Integer, String, Numeric, Boolean, Text, DateTime, func


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    desc = Column(Text, nullable=True)
    price = Column(Numeric(12, 2))
    in_stock = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
