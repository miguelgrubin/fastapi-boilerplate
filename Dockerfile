FROM python:3.11

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --all-extras

RUN mkdir -p /workspace
WORKDIR /workspace
