from django.db import models
from django.contrib.auth.models import AbstractUser
from shared.models import BaseModel

class CustomUser(BaseModel, AbstractUser):
    photo = models.ImageField(upload_to='users/', default='users/default_user_photo.png')
    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True)

    def __str__(self):
        return self.username

