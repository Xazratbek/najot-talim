from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category-detail", kwargs={"pk": self.pk})

    class Meta:
        db_table = "category"
        ordering = ["-id"]
        verbose_name_plural = "Categories"

class Cars(models.Model):
    MAKE = (
        ('bmw', "BMW"),
        ('audi', 'AUDI'),
        ('mers', 'MERS'),
        ('chevrolet', 'Chevrolet')
    )

    model = models.CharField(max_length=29)
    make = models.CharField(max_length=29, choices=MAKE, default="bmw")
    price = models.DecimalField(decimal_places=2, max_digits=7)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='cars/', validators=[FileExtensionValidator(allowed_extensions=['JPG', 'PNG', 'jpg', 'png','JPEG',"jpeg"])])
    year = models.PositiveIntegerField(validators=[MaxValueValidator(2026), MinValueValidator(1885)])
    desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.model

    def get_absolute_url(self):
        return reverse("cars-detail", kwargs={"pk": self.pk})

    class Meta:
        db_table = 'cars'
        ordering = ['-id']
        verbose_name = "Car"
        verbose_name_plural = "Cars"