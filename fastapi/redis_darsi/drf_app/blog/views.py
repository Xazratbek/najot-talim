from django.core.cache import cache
from django.db.models import Count, F
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .cache import POSTS_KEY, POST_COMMENTS_KEY, POST_STATS_KEY, clear_post_cache
from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer, PostStatsSerializer
from .tasks import refresh_post_cache


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        data = cache.get(POSTS_KEY)
        if data is None:
            serializer = self.get_serializer(self.get_queryset(), many=True)
            data = serializer.data
            cache.set(POSTS_KEY, data, 60)
        return Response(data)

    def perform_create(self, serializer):
        serializer.save()
        clear_post_cache()

    def perform_update(self, serializer):
        post = serializer.save()
        clear_post_cache(post.id)

    def perform_destroy(self, instance):
        post_id = instance.id
        instance.delete()
        clear_post_cache(post_id)

    @action(detail=True, methods=["get"], url_path="comments/last")
    def last_comments(self, request, pk=None):
        key = POST_COMMENTS_KEY.format(post_id=pk)
        data = cache.get(key)
        if data is None:
            comments = Comment.objects.filter(post_id=pk).order_by("-created_at")[:10]
            data = CommentSerializer(comments, many=True).data
            cache.set(key, data, 60)
        return Response(data)

    @action(detail=True, methods=["post"])
    def comments(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        clear_post_cache(post.id)
        refresh_post_cache.delay(post.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        Post.objects.filter(pk=pk).update(likes_count=F("likes_count") + 1)
        clear_post_cache(int(pk))
        refresh_post_cache.delay(int(pk))
        return self.stats(request, pk=pk)

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        key = POST_STATS_KEY.format(post_id=pk)
        data = cache.get(key)
        if data is None:
            post = Post.objects.annotate(comments_count=Count("comments")).get(pk=pk)
            data = {
                "post_id": post.id,
                "likes_count": post.likes_count,
                "comments_count": post.comments_count,
            }
            serializer = PostStatsSerializer(data)
            data = serializer.data
            cache.set(key, data, 60)
        return Response(data)
