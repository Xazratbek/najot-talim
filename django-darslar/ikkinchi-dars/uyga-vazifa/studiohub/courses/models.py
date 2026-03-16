from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title