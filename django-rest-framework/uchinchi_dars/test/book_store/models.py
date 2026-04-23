from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    summary = models.TextField(max_length=500, help_text="Kitob haqida qisqacha ma'lumot")
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    published_date = models.DateField()
    pages = models.PositiveIntegerField()

    def __str__(self):
        return self.title
