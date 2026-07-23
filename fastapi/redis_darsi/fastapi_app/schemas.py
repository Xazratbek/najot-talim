from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    body: str


class PostOut(PostCreate):
    id: int
    likes_count: int
    created_at: datetime


class CommentCreate(BaseModel):
    text: str


class CommentOut(CommentCreate):
    id: int
    post_id: int
    created_at: datetime


class PostStats(BaseModel):
    post_id: int
    likes_count: int
    comments_count: int
