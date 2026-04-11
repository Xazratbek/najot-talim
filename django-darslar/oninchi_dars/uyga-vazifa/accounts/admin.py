from django.contrib import admin
from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "phone_number",
        "is_staff",
        "is_active",
        "created_at",
    )
    search_fields = ("username", "email", "phone_number", "first_name", "last_name")
    ordering = ("-id",)
    list_filter = ("is_staff", "is_superuser", "is_active", "created_at")
