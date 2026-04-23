from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    author = models.CharField(max_length=150)
    published_year = models.IntegerField()
    isbn = models.CharField(max_length=13)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "books"