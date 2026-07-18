FROM ghcr.io/astral-sh/uv:0.8.15 AS uv

FROM python:3.13.5-slim-bookworm AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app
COPY --from=uv /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

FROM python:3.13.5-slim-bookworm AS runner

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
RUN useradd --create-home --shell /usr/sbin/nologin app
COPY --from=uv /uv /usr/local/bin/uv
COPY --from=builder /app/.venv /app/.venv
COPY . .
RUN chown -R app:app /app
USER app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
