# Dockerfile
FROM python:3.14-slim

# Evitamos prompts interactivos y configuramos encoding
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema necesarias para Tesseract y Pillow
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-spa \
        libjpeg-dev \
        zlib1g-dev \
        gcc \
        && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Exponer el puerto que usa FastAPI
EXPOSE 10000

# Comando por defecto para correr el bot
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]