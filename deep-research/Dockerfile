FROM python:3.11-slim

# Evita que Python genere .pyc y buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar requirements e instalar
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY app /app

# Variables de entorno (las reales se pasan en docker run o docker-compose)
ENV OPENAI_API_KEY=""
ENV BRAVE_API_KEY=""

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]