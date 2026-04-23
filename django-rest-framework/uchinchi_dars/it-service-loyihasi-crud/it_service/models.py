from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=150,verbose_name="Nomi")
    description = models.TextField(verbose_name="Izox")
    created_at = models.DateTimeField(verbose_name="Yaratilgan vaqti", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Yangilangan vaqti",auto_now=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    title = models.CharField(max_length=250,verbose_name="Sarlavha")
    description = models.TextField(verbose_name="Izox")
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Narxi")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name="Kategoriya",related_name="services")
    is_deleted = models.BooleanField(default=False)
    creator = models.ForeignKey(User,on_delete=models.CASCADE, related_name='services')
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(verbose_name="Yaratilgan vaqti", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Yangilangan vaqti",auto_now=True)

    def __str__(self):
        return self.title