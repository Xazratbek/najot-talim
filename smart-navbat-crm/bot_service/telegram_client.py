"""Minimal Telegram Bot API wrapper — just what the booking flow needs."""

import httpx

API_URL = "https://api.telegram.org/bot{token}/{method}"


async def send_message(bot_token: str, chat_id: int | str, text: str, reply_markup: dict | None = None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    async with httpx.AsyncClient() as client:
        await client.post(API_URL.format(token=bot_token, method="sendMessage"), json=payload, timeout=5.0)


async def answer_callback_query(bot_token: str, callback_query_id: str, text: str | None = None):
    payload = {"callback_query_id": callback_query_id}
    if text:
        payload["text"] = text
    async with httpx.AsyncClient() as client:
        await client.post(
            API_URL.format(token=bot_token, method="answerCallbackQuery"), json=payload, timeout=5.0
        )


def inline_keyboard(buttons: list[list[tuple[str, str]]]) -> dict:
    """buttons: rows of (label, callback_data) tuples."""
    return {
        "inline_keyboard": [
            [{"text": label, "callback_data": data} for label, data in row] for row in buttons
        ]
    }
