from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from mixins import TimeStampMixin
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy import ForeignKey, String, Numeric, Boolean, Integer, Text, func,Enum
from decimal import Decimal
from enum import Enum

if TYPE_CHECKING:
    from models import Product, Category

class OrderStatusChoice(str, Enum):
    PENDING = ("pending","Jarayonda")
    PAID = ("paid","To'langan")
    SHIPPED = ("shipped","Yetkazilmoqda")
    DELIVERED = ("delivered","Yetkazib berilgan")
    CANCELLED = ("cancelled","Bekor qilingan")

    def __new__(cls, value, label):
            obj = str.__new__(cls, value)
            obj._value_ = value
            obj.label = label
            return obj

class User(Base, TimeStampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,index=True)
    username: Mapped[str] = mapped_column(String(150),index=True)
    email: Mapped[str] = mapped_column(String(100),unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean,default=False)

class Category(Base,TimeStampMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    name: Mapped[str] = mapped_column(String(100),unique=True)
    slug: Mapped[str] = mapped_column(String(100),unique=True)


class Product(Base,TimeStampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    name: Mapped[str] = mapped_column(String(250),index=True)
    slug: Mapped[str] = mapped_column(String(250),index=True)
    description: Mapped[Optional[Text]] = mapped_column(Text,nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10,scale=2),index=True)
    stock: Mapped[int] = mapped_column(Integer,default=0)
    image_url: Mapped[Optional[str]] = mapped_column(String(255),nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean,default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id",ondelete="CASCADE"))

class Order(Base,TimeStampMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"))
    total_price: Mapped[Decimal] = mapped_column(Numeric(precision=10,scale=2),default=0)

class OrderItem(Base,TimeStampMixin):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id",ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id",ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column(Integer,default=0)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10,scale=2))

class Wishlist(Base,TimeStampMixin):
    __tablename__ = "wishlists"
    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id",ondelete="CASCADE"))
