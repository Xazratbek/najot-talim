from django.db import models

from tenants.models import Employee, Service, Tenant


class Client(models.Model):
    """An end customer of a tenant, identified by phone and/or Telegram id."""

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="clients")
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    telegram_user_id = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "telegram_user_id"],
                condition=~models.Q(telegram_user_id=""),
                name="unique_client_telegram_id_per_tenant",
            ),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.tenant.name})"


class Appointment(models.Model):
    """A booked slot: the core object the whole product revolves around."""

    class Status(models.TextChoices):
        PENDING = "pending", "Kutilmoqda"
        CONFIRMED = "confirmed", "Tasdiqlangan"
        CANCELLED = "cancelled", "Bekor qilingan"
        COMPLETED = "completed", "Bajarilgan"

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="appointments")
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments"
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="appointments")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "start_time"],
                condition=~models.Q(status="cancelled"),
                name="unique_employee_slot_when_not_cancelled",
            ),
        ]

    def __str__(self):
        return f"{self.client.full_name} — {self.service.name} @ {self.start_time:%Y-%m-%d %H:%M}"
