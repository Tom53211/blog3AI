FROM python:3.14-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

# Install dependencies first (better layer caching)
COPY src/backend/pyproject.toml src/backend/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src/backend/ ./
RUN uv sync --frozen --no-dev

CMD ["uv", "run", "python", "scrape_blogs.py"]
