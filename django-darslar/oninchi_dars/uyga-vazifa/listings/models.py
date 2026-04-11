from django.db import models
from django.urls import reverse
from utils.models import BaseModel
from categories.models import Category
from accounts.models import CustomUser
import uuid

class ConditionChoice(models.TextChoices):
    NEW = "new", "Yangi"
    USED = "used", "B/U"

class StatusChoice(models.TextChoices):
    ACTIVE = "active", "Faol"
    SOLD = "sold", "Sotilgan"
    ARCHIVED = "archived", "Arxivlangan"
    DELETED = "deleted","O'chirilgan"

class CurrencyChoice(models.TextChoices):
    UZS = 'uzs', "So'm"
    USD = 'usd', "USD"
    EUR = "eur", "Euro"

class Listing(BaseModel):
    uuid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    title = models.CharField(max_length=150,verbose_name="Nom",db_index=True)
    description = models.TextField(verbose_name="Tavsif")
    price = models.DecimalField(max_digits=14, decimal_places=2, db_index=True)
    currency = models.CharField(max_length=30, choices=CurrencyChoice.choices, default=CurrencyChoice.UZS, db_index=True)
    listing_category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="category_listings")
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_listings")
    condition = models.CharField(max_length=10, choices=ConditionChoice.choices, default=ConditionChoice.NEW)
    city = models.CharField(max_length=150,db_index=True)
    status = models.CharField(max_length=25, choices=StatusChoice.choices, default=StatusChoice.ACTIVE ,db_index=True)
    view_count = models.PositiveBigIntegerField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("listing:detail", kwargs={"uuid": self.uuid})


    class Meta:
        db_table = "listings"
        verbose_name = "E'lon"
        verbose_name_plural = "E'lonlar"
        indexes = [
            models.Index(fields=["listing_category", "status"],name="listing_category_status_idx"),
            models.Index(fields=["listing_category", "price"],name="listing_category_price_idx"),
            models.Index(fields=["listing_category", "currency"],name="listing_category_currency_idx"),
            models.Index(fields=["city", "status"],name="city_status_idx"),
            models.Index(fields=["created_at", "status"],name="created_at_status_idx"),
        ]

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to="listings/%Y/%m/%d/",default="")
    is_main = models.BooleanField(default=False,verbose_name="Rasm asosiymi")

    def __str__(self):
        return f"{self.listing.title}-ning rasmi"
