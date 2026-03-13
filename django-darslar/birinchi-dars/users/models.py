from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=150)
    birth_year = models.IntegerField(verbose_name="Tug'ilga yili")
    address = models.TextField(verbose_name="Yashash manzili")

    def __str__(self):
        return self.name