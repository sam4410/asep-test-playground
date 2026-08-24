FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY asep/api/ ./asep/api/
COPY asep/db/ ./asep/db/
COPY test_integration.py .
COPY test_performance.py .
COPY test_security.py .

FROM python:3.12-slim AS runner

WORKDIR /app

COPY --from=builder /app /app

RUN useradd -m appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "asep/api/main.py"]
