from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, String, Numeric, Boolean, Integer, Text, ForeignKey, func
from database import Base
from mixins import TimeStampMixin
from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from models import Post, Category, PostView


class User(Base,TimeStampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    username: Mapped[str] = mapped_column(String(50),index=True)
    email: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String)
    is_author: Mapped[bool] = mapped_column(Boolean,default=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="author", lazy="selectin")

class Category(Base,TimeStampMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="category", lazy="selectin")

class Post(Base,TimeStampMixin):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    title: Mapped[str] = mapped_column(String(100))
    slug: Mapped[str] = mapped_column(String(100),unique=True)
    content: Mapped[str] = mapped_column(Text)
    image_url: Mapped[Optional[str]] = mapped_column(String,nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean,default=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id",ondelete="CASCADE"))

    author: Mapped["User"] = relationship(back_populates="posts", lazy="selectin")
    category: Mapped["Category"] = relationship(back_populates="posts", lazy="selectin")
    views: Mapped[list["PostView"]] = relationship(back_populates="post", lazy="selectin")

class PostView(Base,TimeStampMixin):
    __tablename__ = "post_views"
    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id",ondelete="CASCADE"),index=True)

    ip_address: Mapped[Optional[str]] = mapped_column(String(45),nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id",ondelete="SET NULL"), nullable=True)

    post: Mapped["Post"] = relationship(back_populates="views", lazy="selectin")
    viewed_at: Mapped[datetime] = mapped_column(DateTime,default=func.now())

class Comment(Base, TimeStampMixin):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id",ondelete="CASCADE"))
