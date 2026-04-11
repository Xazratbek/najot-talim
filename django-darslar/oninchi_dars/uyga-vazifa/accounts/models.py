from django.db import models
from utils.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser, BaseModel):
    phone_regex = RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Telefon raqami '+998901234567' formatida bo'lishi kerak."
        )
    email = models.EmailField(unique=True)

    avatar = models.ImageField(upload_to="users/%Y/%m/%d/",default="user-default.jpg")
    phone_number = models.CharField(
    validators=[phone_regex],
    max_length=14,
    blank=True,
    verbose_name="Telefon raqami"
    )

    def __str__(self):
        return self.username

    class Meta:
        db_table = "accounts"
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['-id']
        indexes = [
            models.Index(fields=['phone_number'],name='phone_number_idx'),
        ]
