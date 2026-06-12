from sqlalchemy import String,Integer,Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from decimal import Decimal
from app.mixins import TimeStampMixin

class Product(Base,TimeStampMixin):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    make: Mapped[str] = mapped_column(String(50),index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10,scale=2),nullable=False)
