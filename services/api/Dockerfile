FROM python:3.13-slim

WORKDIR /app

COPY services/api/requirements.txt services/api/requirements.txt
RUN pip install --no-cache-dir -r services/api/requirements.txt

COPY services/api/src services/api/src
COPY packages packages

ENV PYTHONPATH=/app/services/api/src
ENV SYNC_DATABASE_URL=postgresql://postgres:dummy_local_password@db:5432/pakimongo_local
ENV UPLOAD_BASE=/app/data/uploads
ENV STORAGE_PROVIDER=local

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
