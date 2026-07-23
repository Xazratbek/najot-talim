from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .cache import POSTS_KEY, POST_COMMENTS_KEY, POST_STATS_KEY, clear_post_cache, get_or_set
from .database import Base, engine, get_db
from .models import Comment, Post
from .schemas import CommentCreate, CommentOut, PostCreate, PostOut, PostStats

app = FastAPI(title="Redis darsi FastAPI")


@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/posts", response_model=list[PostOut])
async def get_posts(db: AsyncSession = Depends(get_db)):
    async def loader():
        result = await db.execute(select(Post).order_by(Post.created_at.desc()))
        return [PostOut.model_validate(post, from_attributes=True).model_dump(mode="json") for post in result.scalars()]

    return await get_or_set(POSTS_KEY, loader)


@app.post("/posts", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(data: PostCreate, db: AsyncSession = Depends(get_db)):
    post = Post(**data.model_dump())
    db.add(post)
    await db.commit()
    await db.refresh(post)
    await clear_post_cache()
    return post


@app.get("/posts/{post_id}/comments/last", response_model=list[CommentOut])
async def get_last_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    async def loader():
        result = await db.execute(
            select(Comment).where(Comment.post_id == post_id).order_by(Comment.created_at.desc()).limit(10)
        )
        return [CommentOut.model_validate(comment, from_attributes=True).model_dump(mode="json") for comment in result.scalars()]

    return await get_or_set(POST_COMMENTS_KEY.format(post_id=post_id), loader)


@app.post("/posts/{post_id}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def create_comment(post_id: int, data: CommentCreate, db: AsyncSession = Depends(get_db)):
    post = await db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post topilmadi")
    comment = Comment(post_id=post_id, **data.model_dump())
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    await clear_post_cache(post_id)
    return comment


@app.post("/posts/{post_id}/like", response_model=PostStats)
async def like_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post topilmadi")
    post.likes_count += 1
    await db.commit()
    await clear_post_cache(post_id)
    return await get_post_stats(post_id, db)


@app.get("/posts/{post_id}/stats", response_model=PostStats)
async def get_post_stats(post_id: int, db: AsyncSession = Depends(get_db)):
    async def loader():
        result = await db.execute(
            select(Post.id, Post.likes_count, func.count(Comment.id))
            .outerjoin(Comment)
            .where(Post.id == post_id)
            .group_by(Post.id)
        )
        row = result.one_or_none()
        if row is None:
            raise HTTPException(status_code=404, detail="Post topilmadi")
        return {"post_id": row[0], "likes_count": row[1], "comments_count": row[2]}

    return await get_or_set(POST_STATS_KEY.format(post_id=post_id), loader)
