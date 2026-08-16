"""Thin async client for the Django public/internal booking API."""

import os

import httpx

DJANGO_API_BASE_URL = os.getenv("DJANGO_API_BASE_URL", "http://localhost:8000/api")
INTERNAL_API_TOKEN = os.getenv("INTERNAL_API_TOKEN", "dev-internal-token")

_bot_token_cache: dict[str, str] = {}


async def get_bot_token(tenant_slug: str) -> str:
    if tenant_slug in _bot_token_cache:
        return _bot_token_cache[tenant_slug]
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DJANGO_API_BASE_URL}/internal/{tenant_slug}/bot-info/",
            headers={"X-Internal-Token": INTERNAL_API_TOKEN},
            timeout=5.0,
        )
        response.raise_for_status()
        token = response.json()["bot_token"]
        _bot_token_cache[tenant_slug] = token
        return token


async def list_services(tenant_slug: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DJANGO_API_BASE_URL}/public/{tenant_slug}/services/", timeout=5.0
        )
        response.raise_for_status()
        return response.json()


async def list_availability(tenant_slug: str, service_id: int, date_str: str) -> list[str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DJANGO_API_BASE_URL}/public/{tenant_slug}/availability/",
            params={"service": service_id, "date": date_str},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()["slots"]


async def create_booking(
    tenant_slug: str,
    service_id: int,
    start_time_iso: str,
    full_name: str,
    telegram_user_id: str,
) -> tuple[int, dict]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DJANGO_API_BASE_URL}/public/{tenant_slug}/book/",
            json={
                "service": service_id,
                "start_time": start_time_iso,
                "client": {
                    "full_name": full_name,
                    "telegram_user_id": telegram_user_id,
                },
            },
            timeout=5.0,
        )
        return response.status_code, response.json()
