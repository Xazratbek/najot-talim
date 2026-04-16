from django.db import models
from django.contrib.auth.models import AbstractUser
from shared.models import BaseModel

class CustomUser(BaseModel, AbstractUser):
    photo = models.ImageField(upload_to='users/', default='users/default_user_photo.png')
    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True)

    def __str__(self):
        return self.username


class Cash(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='balance')
    card_number = models.PositiveIntegerField()
    card_date = models.DateField()
    cvv = models.PositiveIntegerField(null=True, blank=True)
    ammount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    def __str__(self):
        return self.user.username



