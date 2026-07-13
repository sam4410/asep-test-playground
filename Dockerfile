FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.12-slim AS runner

WORKDIR /app

COPY --from=builder /app /app

RUN useradd -m appuser
USER appuser

ENV FLASK_APP=routes/auth.py
ENV DATABASE_URL=sqlite:///app.db
ENV SECRET_KEY=your_secret_key

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
