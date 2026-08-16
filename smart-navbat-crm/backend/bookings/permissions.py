from django.conf import settings
from rest_framework.permissions import BasePermission


class IsInternalService(BasePermission):
    """Grants access only to requests carrying the shared internal token.

    Used for the bot-info endpoint, which exposes a tenant's Telegram bot
    token — that's internal wiring for the bot_service, not public data.
    """

    def has_permission(self, request, view):
        token = request.headers.get("X-Internal-Token", "")
        return bool(token) and token == settings.INTERNAL_API_TOKEN
