# Use official UV image for better performance
FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS builder

WORKDIR /app

# Copy configuration files
COPY pyproject.toml uv.lock ./

# UV optimizations for faster builds and startup
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Install dependencies with BuildKit cache mounts
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=/app/uv.lock \
    --mount=type=bind,source=pyproject.toml,target=/app/pyproject.toml \
    uv sync --frozen --no-dev

# Copy source code
COPY src /app/src
COPY main.py /app/

# Production stage
FROM python:3.12-slim AS production

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Copy virtual environment and application from builder
COPY --from=builder /app /app

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1

# Version argument for build-time configuration
ARG VERSION=0.1.0
ENV APP_VERSION=$VERSION

# Change ownership to app user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Expose port
EXPOSE 8000

# Use uvicorn with multiple workers for production performance
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]