from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    color = models.CharField(max_length=50)
    warranty_months = models.IntegerField(default=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product"
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"