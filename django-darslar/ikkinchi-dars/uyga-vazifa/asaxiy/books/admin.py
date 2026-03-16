from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'price', 'created_at')
    search_fields = ('name', 'author')
    list_filter = ('created_at', 'price')
    ordering = ('-created_at',)
