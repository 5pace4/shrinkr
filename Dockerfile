# syntax=docker/dockerfile:1

FROM python:3.14-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

# cassandra-driver has C extensions; build tools + libev headers are needed
# to compile them if no prebuilt wheel exists for this Python/arch.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libev-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first so this layer stays cached across source-only changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY src ./src
COPY README.md ./
# --no-editable: bake the package into site-packages so the runtime image
# doesn't need the source tree, only the resulting virtualenv.
RUN uv sync --frozen --no-dev --no-editable


FROM python:3.14-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    libev4 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1000 shrinkr

WORKDIR /app

COPY --from=builder --chown=shrinkr:shrinkr /app/.venv ./.venv

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

USER shrinkr

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=5 \
    CMD curl -sf http://127.0.0.1:8000/api/health/ || exit 1

CMD ["uvicorn", "shrinkr.main:app", "--host", "0.0.0.0", "--port", "8000"]
