FROM python:3.14-slim

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies (including dev for debugpy)
RUN uv sync --frozen

# Copy application source code
COPY main.py ./
COPY src ./src

# Expose ports
EXPOSE 8000
EXPOSE 5678

# Run the application with uvicorn
CMD ["uv", "run", "main.py", "http-server"]