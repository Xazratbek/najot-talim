from shared.models import BaseModel
from django.db import models

class Slider(BaseModel):
    image = models.ImageField(upload_to="sliders/%Y/%m/%d/")
    title = models.CharField(max_length=300)
    description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.title

class Banner(BaseModel):
    image = models.ImageField(upload_to="banners/%Y/%m/%d/")
    url = models.URLField()
    position = models.CharField(max_length=350)

    def __str__(self):
        return f"Banner at: {self.position}"

class Brand(BaseModel):
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to="brands/%Y/%m/%d/")

    def __str__(self):
        return self.name