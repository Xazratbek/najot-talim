from decimal import Decimal

from django.db import models
from django.db.models import DecimalField, F, Sum, Value
from django.db.models.functions import Coalesce

from django.conf import settings

from utils.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Telefon(BaseModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='phones'
    )
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="phone/%Y/%M/%d/",null=True,blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    ram = models.PositiveIntegerField(help_text="GB da")
    storage = models.PositiveIntegerField(help_text="GB da")
    battery = models.PositiveIntegerField(help_text="mAh")
    display_size = models.DecimalField(max_digits=4, decimal_places=2, help_text="inch")
    main_camera = models.CharField(max_length=100, help_text="108MP")
    front_camera = models.CharField(max_length=100, help_text="32MP")
    is_available = models.BooleanField(default=True)
    color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.brand} {self.name}"

class Status(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    CANCELLED = "cancelled", "Cancelled"
    DELIVERED = "delivered", "Delivered"

class Order(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.total_price is None:
            self.total_price = Decimal("0.00")
        super().save(*args, **kwargs)

    def recalculate_total_price(self):
        total = self.items.aggregate(
            total=Coalesce(
                Sum(
                    F("price") * F("quantity"),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                ),
                Value(Decimal("0.00")),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        )["total"]
        self.total_price = total
        self.save(update_fields=["total_price"])

    def __str__(self):
        return f"Order #{self.id} - {self.user}"


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    telefon = models.ForeignKey(
        "Telefon",
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        previous_order_id = None
        previous_telefon_id = None

        if self.pk:
            previous_item = OrderItem.objects.filter(pk=self.pk).values(
                "order_id",
                "telefon_id",
            ).first()
            if previous_item:
                previous_order_id = previous_item["order_id"]
                previous_telefon_id = previous_item["telefon_id"]

        if self.telefon_id and (not self.pk or previous_telefon_id != self.telefon_id or self.price is None):
            self.price = self.telefon.price

        super().save(*args, **kwargs)
        self.order.recalculate_total_price()

        if previous_order_id and previous_order_id != self.order_id:
            previous_order = Order.objects.filter(pk=previous_order_id).first()
            if previous_order:
                previous_order.recalculate_total_price()

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        order.recalculate_total_price()
