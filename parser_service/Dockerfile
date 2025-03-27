FROM python:3.10-slim

WORKDIR /app

COPY parser_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY parser_service . 
COPY database ./database

CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
