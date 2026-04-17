from django.db import models
from users.models import CustomUser
from shared.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

class Category(BaseModel):
    title = models.CharField(max_length=120)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_category')

    def __str__(self):
        return self.title

class Product(BaseModel):
    title = models.CharField(max_length=120)
    desc = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    discount = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(99), MinValueValidator(5)])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    is_featured = models.BooleanField(default=False)

    @property
    def final_price(self):
        if self.discount:
            return self.price * (Decimal(100) - Decimal(self.discount)) / Decimal(100)
        return self.price

    def __str__(self):
        return self.title


class ProductImage(BaseModel):
    photo = models.ImageField(upload_to='products/', default='products/default_image.png', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        if self.product.images.count() >= 5:
            raise ValidationError('5 tadan kop rasm qabul qilinmaydi')
        super().save(*args, **kwargs)


class Comment(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=120, blank=True, null=True)
    rate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)

    def __str__(self):
        return f"{self.user.username}|||{self.product.title}"

    class Meta:
        unique_together = ['user', 'product']


class Saved(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='saved_users')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved_products')

    def __str__(self):
        return f"{self.user.username}|||{self.product.title}"

    class Meta:
        unique_together = ['user', 'product']

class RecentlyProduct(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recently_products')

    def __str__(self):
        return f"{self.user.username}|||{self.product.title}"

    class Meta:
        unique_together = ['user', 'product']


class ProductView(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='view_product')

    def __str__(self):
        return f"{self.product.title}"

class PromoCode(BaseModel):
    DISCOUNT_TYPE = (
        ('percent', 'Percent'),
        ('fixed', 'Fixed'),
    )

    PROMO_TYPE = (
        ('welcome', 'Welcome'),
        ('public', 'Public'),
        ('personal','Personal'),
    )
    title = models.CharField(max_length=150, help_text="Promo code turi masalan: Birinchi xarid uchun 30 000 so'm sovg'a")
    code = models.CharField(max_length=50, unique=True,db_index=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE, default='percent')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    promo_type = models.CharField(max_length=30,choices=PROMO_TYPE,default='welcome')
    is_active = models.BooleanField(default=True)
    expire_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.code}"

    @staticmethod
    def apply_discount(discount_type, discount_value, summa):
        summa = Decimal(summa)
        discount_value = Decimal(discount_value)

        if discount_type == 'percent':
            chegirma = (summa * discount_value) / Decimal(100)
        else:
            chegirma = discount_value

        return summa - chegirma

class PromoCodeUsage(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='promo_usages')
    promocode = models.ForeignKey(PromoCode, on_delete=models.CASCADE, related_name='usages')
    usage_count = models.PositiveIntegerField(default=0)
    last_used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'promocode')

    def __str__(self):
        return f"{self.user.username} - {self.promocode.code} ({self.usage_count})"
