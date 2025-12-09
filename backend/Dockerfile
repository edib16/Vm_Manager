# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# 1. Installation des outils système (libvirt)
RUN apt-get update && apt-get install -y \
    pkg-config \
    libvirt-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 2. Installation Python
# Note : On copie depuis "backend/" car le contexte sera la racine
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn

# 3. Copie du code et du .env
COPY backend/ ./backend
# On copie le .env qui est à la racine
#COPY .env .

# 4. Config
ENV PYTHONPATH=/app/backend
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "backend.main:app"]
