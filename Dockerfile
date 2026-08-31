# syntax=docker/dockerfile:1.7

########################
# ---- Builder stage ---
########################
FROM python:3.12.7-slim-bookworm AS builder

# Prevent Python from writing pyc files & enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install build dependencies only where needed (kept minimal)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into an isolated prefix for easy copy
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Copy application source (adjust if entry point/module structure changes)
COPY . .


########################
# ---- Runtime stage ---
########################
FROM python:3.12.7-slim-bookworm AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/usr/local/bin:$PATH" \
    APP_HOME=/app

# Install curl for HEALTHCHECK only (kept minimal, removed after use is not possible
# since curl binary is required at runtime for HEALTHCHECK; keep it slim)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user and group
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /usr/sbin/nologin --create-home appuser

WORKDIR ${APP_HOME}

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY --from=builder /build ${APP_HOME}

# Ensure non-root user owns the application directory
RUN chown -R appuser:appgroup ${APP_HOME}

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production entry point.
# NOTE: No framework/entry point was detected in the workspace.
# Update this CMD to match your actual application entry point
# (e.g. gunicorn app:app --bind 0.0.0.0:8000, or python main.py).
CMD ["python", "-m", "app"]
