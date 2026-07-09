"""Telegram webhook service for the Smart Navbat CRM booking flow.

One Telegram update in, one of a handful of booking-flow steps handled.
This is intentionally a small hand-rolled FSM rather than a full framework
like aiogram/python-telegram-bot's dispatcher — the conversation is short
(pick service -> pick day -> pick slot -> give name -> confirm), and this
keeps the whole service to one file that's easy to read end to end.
"""

from datetime import date, timedelta

from fastapi import FastAPI, Request

from django_client import create_booking, get_bot_token, list_availability, list_services
from state import get_state, reset_state
from telegram_client import answer_callback_query, inline_keyboard, send_message

app = FastAPI(title="Smart Navbat CRM — Telegram Bot Service")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/webhook/{tenant_slug}")
async def telegram_webhook(tenant_slug: str, request: Request):
    update = await request.json()
    bot_token = await get_bot_token(tenant_slug)
    if not bot_token:
        return {"ok": False, "error": "tenant has no bot token configured"}

    if "callback_query" in update:
        await _handle_callback(tenant_slug, bot_token, update["callback_query"])
    elif "message" in update:
        await _handle_message(tenant_slug, bot_token, update["message"])

    return {"ok": True}


async def _handle_message(tenant_slug: str, bot_token: str, message: dict):
    chat_id = message["chat"]["id"]
    text = (message.get("text") or "").strip()
    state = get_state(tenant_slug, chat_id)

    if text == "/start":
        reset_state(tenant_slug, chat_id)
        await _send_service_menu(tenant_slug, bot_token, chat_id)
        return

    if state["step"] == "awaiting_name" and text:
        await _finalize_booking(tenant_slug, bot_token, chat_id, full_name=text)
        return

    await send_message(bot_token, chat_id, "Boshlash uchun /start buyrug'ini yuboring.")


async def _handle_callback(tenant_slug: str, bot_token: str, callback_query: dict):
    chat_id = callback_query["message"]["chat"]["id"]
    data = callback_query.get("data", "")
    await answer_callback_query(bot_token, callback_query["id"])

    if data.startswith("svc:"):
        service_id = int(data.split(":", 1)[1])
        state = get_state(tenant_slug, chat_id)
        state["step"] = "awaiting_date"
        state["service_id"] = service_id
        await _send_date_menu(bot_token, chat_id)

    elif data.startswith("date:"):
        chosen_date = data.split(":", 1)[1]
        state = get_state(tenant_slug, chat_id)
        state["step"] = "awaiting_slot"
        state["date"] = chosen_date
        await _send_slot_menu(tenant_slug, bot_token, chat_id, state["service_id"], chosen_date)

    elif data.startswith("slot:"):
        slot_iso = data.split(":", 1)[1]
        state = get_state(tenant_slug, chat_id)
        state["step"] = "awaiting_name"
        state["slot"] = slot_iso
        await send_message(bot_token, chat_id, "Ismingizni yuboring (F.I.Sh):")


async def _send_service_menu(tenant_slug: str, bot_token: str, chat_id: int):
    services = await list_services(tenant_slug)
    if not services:
        await send_message(bot_token, chat_id, "Hozircha xizmatlar mavjud emas.")
        return
    rows = [[(f"{s['name']} ({s['duration_minutes']} min)", f"svc:{s['id']}")] for s in services]
    await send_message(bot_token, chat_id, "Qaysi xizmatga yozilmoqchisiz?", inline_keyboard(rows))


async def _send_date_menu(bot_token: str, chat_id: int):
    today = date.today()
    rows = [
        [((today + timedelta(days=offset)).strftime("%d-%m (%a)"), f"date:{(today + timedelta(days=offset)).isoformat()}")]
        for offset in range(7)
    ]
    await send_message(bot_token, chat_id, "Qaysi kunga yozilmoqchisiz?", inline_keyboard(rows))


async def _send_slot_menu(tenant_slug: str, bot_token: str, chat_id: int, service_id: int, chosen_date: str):
    slots = await list_availability(tenant_slug, service_id, chosen_date)
    if not slots:
        await send_message(bot_token, chat_id, "Bu kunda bo'sh vaqt yo'q. Boshqa kunni tanlang: /start")
        return
    rows = [[(_format_slot(slot), f"slot:{slot}")] for slot in slots]
    await send_message(bot_token, chat_id, "Bo'sh vaqtni tanlang:", inline_keyboard(rows))


def _format_slot(slot_iso: str) -> str:
    return slot_iso.replace("T", " ")[:16]


async def _finalize_booking(tenant_slug: str, bot_token: str, chat_id: int, full_name: str):
    state = get_state(tenant_slug, chat_id)
    status_code, data = await create_booking(
        tenant_slug=tenant_slug,
        service_id=state["service_id"],
        start_time_iso=state["slot"],
        full_name=full_name,
        telegram_user_id=str(chat_id),
    )
    if status_code == 201:
        when = _format_slot(state["slot"])
        await send_message(bot_token, chat_id, f"Rahmat, {full_name}! Siz {when} vaqtga yozildingiz.")
    elif status_code == 409:
        await send_message(bot_token, chat_id, "Afsuski bu vaqt band bo'lib qoldi. Qayta urinib ko'ring: /start")
    else:
        await send_message(bot_token, chat_id, "Xatolik yuz berdi. Iltimos qayta urinib ko'ring: /start")

    reset_state(tenant_slug, chat_id)
