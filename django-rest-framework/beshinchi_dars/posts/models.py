from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    author = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
