from django.db import models

class Laptop(models.Model):
    brand = models.CharField(max_length=150)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    cpu = models.CharField(max_length=255)
    gpu = models.CharField(max_length=255, blank=True)
    ram = models.PositiveIntegerField(help_text="GB")
    storage = models.PositiveIntegerField(help_text="GB")
    storage_type = models.CharField(max_length=50, choices=[
        ('ssd', 'SSD'),
        ('hdd', 'HDD'),
    ])
    image = models.ImageField(upload_to="laptop/%Y/%M/%d/",blank=True, null=True)

    screen_size = models.DecimalField(max_digits=4, decimal_places=1)
    resolution = models.CharField(max_length=50)

    battery = models.PositiveIntegerField(help_text="mAh", blank=True, null=True)

    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="kg")

    os = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name