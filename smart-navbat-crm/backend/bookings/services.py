"""Booking domain logic: slot availability and Telegram notifications.

Kept deliberately simple for the MVP — no Celery/queue worker, since the
target infra budget in the research doc is ~$20-30/month. Notifications are
sent synchronously (best-effort, failures are logged, never block booking).
"""

import logging
from datetime import datetime, time, timedelta

import httpx
from django.utils import timezone

from .models import Appointment

logger = logging.getLogger(__name__)

BUSINESS_DAY_START = time(9, 0)
BUSINESS_DAY_END = time(20, 0)
TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def get_available_slots(service, target_date, employee=None):
    """Return free start-time slots for a service on a given date.

    Naive fixed-hours model (09:00-20:00) minus already-booked slots for
    the chosen employee (or the whole tenant if no employee is specified).
    Good enough for the MVP; a per-tenant working-hours model is a
    natural post-MVP addition.
    """
    duration = timedelta(minutes=service.duration_minutes)
    day_start = timezone.make_aware(datetime.combine(target_date, BUSINESS_DAY_START))
    day_end = timezone.make_aware(datetime.combine(target_date, BUSINESS_DAY_END))

    booked_qs = Appointment.objects.filter(
        tenant=service.tenant,
        start_time__gte=day_start,
        start_time__lt=day_end,
    ).exclude(status=Appointment.Status.CANCELLED)
    if employee is not None:
        booked_qs = booked_qs.filter(employee=employee)
    booked_starts = set(booked_qs.values_list("start_time", flat=True))

    slots = []
    cursor = day_start
    now = timezone.now()
    while cursor + duration <= day_end:
        if cursor > now and cursor not in booked_starts:
            slots.append(cursor)
        cursor += duration
    return slots


def send_telegram_message(bot_token, chat_id, text):
    if not bot_token or not chat_id:
        return
    try:
        response = httpx.post(
            TELEGRAM_API_URL.format(token=bot_token),
            json={"chat_id": chat_id, "text": text},
            timeout=5.0,
        )
        response.raise_for_status()
    except httpx.HTTPError:
        logger.exception("Telegram xabarnomasi yuborilmadi (chat_id=%s)", chat_id)


def notify_new_appointment(appointment):
    """Notify the client and the assigned employee about a new booking."""
    tenant = appointment.tenant
    bot_token = tenant.telegram_bot_token
    when = timezone.localtime(appointment.start_time).strftime("%Y-%m-%d %H:%M")

    if appointment.client.telegram_user_id:
        send_telegram_message(
            bot_token,
            appointment.client.telegram_user_id,
            f"Assalomu alaykum, {appointment.client.full_name}!\n"
            f"Siz \"{appointment.service.name}\" xizmatiga {when} vaqtga yozildingiz.\n"
            f"{tenant.name} sizni kutmoqda.",
        )

    if appointment.employee and appointment.employee.telegram_chat_id:
        send_telegram_message(
            bot_token,
            appointment.employee.telegram_chat_id,
            f"Yangi band: {appointment.client.full_name} — "
            f"{appointment.service.name}, {when}.",
        )
