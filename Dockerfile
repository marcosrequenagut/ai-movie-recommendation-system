FROM python:3.9-slim

# Evita logs raros y mejora rendimiento
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema (opcional pero recomendable para pandas/psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (mejor cache de Docker)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Puerto de FastAPI
EXPOSE 8000

# Comando por defecto (puede ser sobreescrito por docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]