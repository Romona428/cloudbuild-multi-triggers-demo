FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

ENV TIMEOUT=120

EXPOSE 8080
CMD ["sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker app:app -b 0.0.0.0:${PORT:-8080} --timeout ${TIMEOUT}"]
