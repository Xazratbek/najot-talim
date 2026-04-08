from django.contrib import admin
from .models import Product, ProductImage, Category

admin.site.register(Category)

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ["id","name","created_at","updated_at"]
#     list_filter = ["created_at"]
#     ordering = ['-id']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ["id","name","brand","category","price","stock"]
    list_filter = ["category","brand"]
    search_fields = ["name","description"]