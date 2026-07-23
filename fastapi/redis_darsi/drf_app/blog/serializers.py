from rest_framework import serializers

from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "body", "likes_count", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "text", "created_at"]
        read_only_fields = ["post"]


class PostStatsSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    likes_count = serializers.IntegerField()
    comments_count = serializers.IntegerField()
