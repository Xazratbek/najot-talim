from django.contrib import admin
from listings.models import Listing, ListingImage

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 6

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    inlines = [ListingImageInline]
    list_display = (
        "uuid",
        "title",
        "listing_category",
        "user",
        "price",
        "currency",
        "city",
        "status",
        "view_count",
        "created_at",
    )
    search_fields = ("title", "description", "city", "user__username", "listing_category__name")
    ordering = ("-created_at",)
    list_filter = (
        "status",
        "condition",
        "currency",
        "city",
        "listing_category",
        "created_at",
    )


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "is_main")
    search_fields = ("listing__title",)
    ordering = ("-id",)
    list_filter = ("is_main",)
