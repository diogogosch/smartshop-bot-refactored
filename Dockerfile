FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN ls -la /app && ls -la /app/app && test -f /app/app/main.py

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "-m", "app.main"]
