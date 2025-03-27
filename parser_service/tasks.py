import os
from celery import Celery
from parser import parse_document

REDIS_URL = os.getenv("REDIS_URL")

app = Celery('tasks', broker=REDIS_URL)

@app.task
def parse_file_task(file_path, document_id):
    return parse_document(file_path, document_id)
