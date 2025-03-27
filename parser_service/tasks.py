from celery import Celery
from parser import parse_document

app = Celery('tasks', broker='redis://redis:6379/0')

@app.task
def parse_file_task(file_path, document_id):
    return parse_document(file_path, document_id)