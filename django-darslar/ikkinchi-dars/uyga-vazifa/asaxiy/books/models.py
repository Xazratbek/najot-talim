from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Kitob"
        verbose_name_plural = "Kitoblar"
