from .models import Post

def get_latest_posts():
    return Post.objects.all().order_by('-created_at')[:10]