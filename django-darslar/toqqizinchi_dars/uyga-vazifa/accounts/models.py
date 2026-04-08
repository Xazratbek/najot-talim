from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    avatar = models.ImageField(upload_to="users/%Y/%m/%d/",null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "customusers"
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"