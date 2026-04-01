from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id","name","created_at"]
    list_filter = ["name"]

@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ["id","model","make","price","category"]
    search_fields = ['model','make']
    ordering = ["-id"]