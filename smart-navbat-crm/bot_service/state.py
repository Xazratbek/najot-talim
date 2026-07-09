"""In-memory per-chat conversation state.

Good enough for an MVP demo/pilot; a real deployment should move this to
Redis so state survives a bot_service restart and works across replicas.
"""

STATE: dict[tuple[str, int], dict] = {}


def get_state(tenant_slug: str, chat_id: int) -> dict:
    return STATE.setdefault((tenant_slug, chat_id), {"step": "idle"})


def reset_state(tenant_slug: str, chat_id: int) -> dict:
    STATE[(tenant_slug, chat_id)] = {"step": "idle"}
    return STATE[(tenant_slug, chat_id)]
