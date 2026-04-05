from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to="users/", null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=13, validators=[RegexValidator(regex=r"^\+?998\s?(33|77|88|90|91|93|94|95|97|98|99|71|66)[0-9]{7}$",message="Faqat o'zbekiston aloqa operatorlaridan foydalanib ro'yxatdan o'tish mumkin.")], null=True, blank=True)

    def __str__(self):
        return self.username