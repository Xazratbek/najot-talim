from django.core.cache import cache

POSTS_KEY = "drf:posts:list"
POST_COMMENTS_KEY = "drf:posts:{post_id}:comments:last10"
POST_STATS_KEY = "drf:posts:{post_id}:stats"


def clear_post_cache(post_id=None):
    cache.delete(POSTS_KEY)
    if post_id is not None:
        cache.delete_many([POST_COMMENTS_KEY.format(post_id=post_id), POST_STATS_KEY.format(post_id=post_id)])
