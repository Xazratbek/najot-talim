from django.db import models

# books_categorys
# Categorys
class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        db_table = "categories"


class Author(models.Model):
    name = models.CharField(max_length=500)
    dob = models.DateField()
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "authors"

class Book(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    author = models.ForeignKey(Author,blank=True, null=True, on_delete=models.SET_NULL)
    published_year = models.IntegerField()
    isbn = models.CharField(max_length=13)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "books"

class BookCategories(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Kitob: {self.book.title} Category: {self.category.name}"

    class Meta:
        db_table = "book_categories"
        verbose_name_plural = "Book Categories"