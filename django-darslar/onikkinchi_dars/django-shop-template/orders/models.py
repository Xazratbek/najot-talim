from django.db import models
from shared.models import BaseModel
from users.models import CustomUser
from products.models import Product
# Create your models here.


class Card(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True, related_name='card')

    def __str__(self):
        return self.user.username

class CardItem(BaseModel):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.product:
            self.total_price = self.product.final_price * self.quantity
        else:
            self.total_price = 0
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['product', 'card']



class Order(BaseModel):
    STATUS = (
        ('new', 'New'),
        ('paid', 'Paid'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=120)
    status = models.CharField(max_length=20, choices=STATUS, default='new')

    @property
    def finished_price(self):
        return sum(i.total_price for i in self.items)

    def __str__(self):
        return self.user.username


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='products')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.order.user.username
