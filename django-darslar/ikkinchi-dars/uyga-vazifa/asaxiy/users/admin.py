from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at', 'age')
    ordering = ('-created_at',)
