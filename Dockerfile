FROM python:3.14-slim

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application source code
COPY main.py ./
COPY src ./src

# Expose port
EXPOSE 8000

# Run the application with uvicorn
CMD ["uv", "run", "main.py", "http-server"]
