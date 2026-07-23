from celery import shared_task
from django.core.cache import cache
from django.db.models import Count

from .cache import POST_COMMENTS_KEY, POST_STATS_KEY
from .models import Comment, Post
from .serializers import CommentSerializer


@shared_task
def refresh_post_cache(post_id):
    post = Post.objects.annotate(comments_count=Count("comments")).get(pk=post_id)
    stats = {
        "post_id": post.id,
        "likes_count": post.likes_count,
        "comments_count": post.comments_count,
    }
    cache.set(POST_STATS_KEY.format(post_id=post_id), stats, 60)

    comments = Comment.objects.filter(post_id=post_id).order_by("-created_at")[:10]
    cache.set(POST_COMMENTS_KEY.format(post_id=post_id), CommentSerializer(comments, many=True).data, 60)
    return stats
