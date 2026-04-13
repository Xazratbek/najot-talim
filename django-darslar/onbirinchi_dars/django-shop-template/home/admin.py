from django.contrib import admin
from .models import Slider, Banner, Brand

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['id',"title","description","url"]
    search_fields = ["title","description"]
    ordering = ['-id']

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id','url','position']
    search_fields = ['position']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    ordering = ['name']