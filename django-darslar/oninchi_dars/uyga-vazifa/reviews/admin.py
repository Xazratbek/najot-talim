from django.contrib import admin
from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "reviewer", "target_user", "rating", "created_at")
    search_fields = (
        "reviewer__username",
        "reviewer__email",
        "target_user__username",
        "target_user__email",
        "comment",
    )
    ordering = ("-created_at",)
    list_filter = ("rating", "created_at", "updated_at")
