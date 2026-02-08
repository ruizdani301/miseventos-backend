FROM python:3.12.8-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN pip install poetry==2.2.1

WORKDIR /app

# Copiar SOLO los archivos necesarios para poetry install
COPY pyproject.toml .
COPY README.md .
COPY poetry.lock ./

# Por esta (agrega --no-root):
RUN poetry config virtualenvs.create false && \
    poetry install --only=main --no-interaction --no-ansi --no-root

# Ahora copiar TODO el código restante
COPY . .

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app:/app/src"

# Crear usuario no-root
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -u 1000 appuser && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.miseventos.main:app", "--host", "0.0.0.0", "--port", "8000"]