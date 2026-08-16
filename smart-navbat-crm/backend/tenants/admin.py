from django.contrib import admin

from .models import Employee, Service, Tenant


class TenantScopedAdmin(admin.ModelAdmin):
    """Base admin that restricts non-superusers to their own tenant's rows.

    The MVP CRM dashboard *is* the Django admin: each business owner is a
    staff user with exactly one Tenant, so scoping every queryset by
    `request.user.tenant` is what keeps one business from ever seeing
    another business's clients or appointments.
    """

    tenant_field = "tenant"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if not hasattr(request.user, "tenant"):
            return qs.none()
        return qs.filter(**{self.tenant_field: request.user.tenant})

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not change:
            setattr(obj, self.tenant_field, request.user.tenant)
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, "tenant"):
            if db_field.name == self.tenant_field:
                kwargs["queryset"] = Tenant.objects.filter(pk=request.user.tenant.pk)
            elif db_field.name in ("employee", "service"):
                related_model = db_field.remote_field.model
                kwargs["queryset"] = related_model.objects.filter(tenant=request.user.tenant)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "plan", "is_active", "created_at")
    list_filter = ("plan", "is_active")
    search_fields = ("name", "slug", "phone")
    prepopulated_fields = {"slug": ("name",)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)


@admin.register(Employee)
class EmployeeAdmin(TenantScopedAdmin):
    list_display = ("full_name", "position", "tenant", "is_active")
    list_filter = ("tenant", "is_active")
    search_fields = ("full_name",)


@admin.register(Service)
class ServiceAdmin(TenantScopedAdmin):
    list_display = ("name", "tenant", "duration_minutes", "price", "is_active")
    list_filter = ("tenant", "is_active")
    search_fields = ("name",)
