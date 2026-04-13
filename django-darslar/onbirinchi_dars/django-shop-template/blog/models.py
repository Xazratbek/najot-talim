from django.db import models
from shared.models import BaseModel
from users.models import CustomUser

class Post(BaseModel):
    title = models.CharField(max_length=150)
    content = models.TextField()
    image = models.ImageField(upload_to="blog/%Y/%m/%d/")

    def __str__(self):
        return f"Maqola: {self.title}"