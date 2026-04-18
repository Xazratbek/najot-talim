from django.db import models

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
    photo = models.ImageField(upload_to='cars/',null=True,blank=True)
    year = models.PositiveIntegerField()
    desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.model

    class Meta:
        db_table = 'cars'
        ordering = ['-id']
        verbose_name = "Car"
        verbose_name_plural = "Cars"