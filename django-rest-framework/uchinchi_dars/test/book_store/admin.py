from django.contrib import admin
from .models import Book,Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name','birth_date']
    ordering = ['-id']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title','author','summary','isbn','published_date','pages']
    list_filter = ['published_date']
    ordering = ['-id']
