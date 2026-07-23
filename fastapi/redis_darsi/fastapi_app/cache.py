import json
import os
from collections.abc import Awaitable, Callable
from typing import TypeVar

from redis.asyncio import Redis

T = TypeVar("T")

redis = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"), decode_responses=True)

POSTS_KEY = "fastapi:posts:list"
POST_COMMENTS_KEY = "fastapi:posts:{post_id}:comments:last10"
POST_STATS_KEY = "fastapi:posts:{post_id}:stats"


async def get_or_set(key: str, loader: Callable[[], Awaitable[T]], expire: int = 60) -> T:
    cached = await redis.get(key)
    if cached is not None:
        return json.loads(cached)
    value = await loader()
    await redis.set(key, json.dumps(value, default=str), ex=expire)
    return value


async def clear_post_cache(post_id: int | None = None) -> None:
    await redis.delete(POSTS_KEY)
    if post_id is not None:
        await redis.delete(POST_COMMENTS_KEY.format(post_id=post_id), POST_STATS_KEY.format(post_id=post_id))
