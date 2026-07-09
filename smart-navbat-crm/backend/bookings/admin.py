from django.contrib import admin

from tenants.admin import TenantScopedAdmin

from .models import Appointment, Client


@admin.register(Client)
class ClientAdmin(TenantScopedAdmin):
    list_display = ("full_name", "phone", "tenant", "created_at")
    list_filter = ("tenant",)
    search_fields = ("full_name", "phone", "telegram_user_id")


@admin.register(Appointment)
class AppointmentAdmin(TenantScopedAdmin):
    list_display = (
        "client",
        "service",
        "employee",
        "tenant",
        "start_time",
        "status",
    )
    list_filter = ("tenant", "status", "employee")
    search_fields = ("client__full_name", "notes")
    date_hierarchy = "start_time"
