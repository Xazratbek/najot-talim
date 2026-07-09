from django.conf import settings
from django.db import models


class Tenant(models.Model):
    """A paying business on the platform (o'quv markazi, salon, klinika...)."""

    class Plan(models.TextChoices):
        START = "start", "Start — 150,000 UZS/oy"
        PRO = "pro", "Pro — 300,000 UZS/oy"

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tenant",
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=80, unique=True, help_text="Booking link: /b/<slug>/")
    phone = models.CharField(max_length=20, blank=True)
    telegram_bot_token = models.CharField(
        max_length=200,
        blank=True,
        help_text="Ushbu biznesning o'z Telegram boti tokeni (BotFather).",
    )
    plan = models.CharField(max_length=10, choices=Plan.choices, default=Plan.START)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Employee(models.Model):
    """A staff member (usta/shifokor/o'qituvchi) who can be booked."""

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="employees")
    full_name = models.CharField(max_length=150)
    position = models.CharField(max_length=100, blank=True)
    telegram_chat_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Yangi bandlar haqida xabar oladigan Telegram chat ID.",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.tenant.name})"


class Service(models.Model):
    """A bookable service offered by a tenant (masalan, "Tish tozalash")."""

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=150)
    duration_minutes = models.PositiveIntegerField(default=30)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} — {self.tenant.name}"
