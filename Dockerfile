FROM python:3.13-slim AS builder

WORKDIR /app
COPY services/api/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt gunicorn

FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY services/api/ .
COPY packages/scoring-rules /app/packages/scoring-rules

ENV PYTHONPATH=/app/src
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health/live || exit 1

CMD ["gunicorn", "src.main:app", "-c", "gunicorn.conf.py"]
