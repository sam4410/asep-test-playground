FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd --create-home --shell /bin/bash asep

COPY pyproject.toml README.md ./
COPY asep ./asep
COPY migrations ./migrations
COPY alembic.ini ./
COPY static ./static
COPY tests ./tests

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .[dev]

RUN mkdir -p /app/.asep/artifacts \
    && chown -R asep:asep /app

CMD ["sh", "-c", "uvicorn asep.api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
