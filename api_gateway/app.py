import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from celery import Celery
from database.models import Slide
from database.models import Document
from database.db import SessionLocal 
import requests

# --- App and Config ---
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'pptx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Celery Config ---
REDIS_URL = os.getenv("REDIS_URL")
celery_app = Celery('tasks', broker=REDIS_URL)

# --- Helpers ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Routes ---
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # File size limit check (e.g. 10MB)
    MAX_FILE_SIZE_MB = 10  # Limit to 10MB
    MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024

    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)

    if file_length > MAX_FILE_SIZE:
        return jsonify({'error': f'File exceeds {MAX_FILE_SIZE_MB}MB limit.'}), 400
    # 
    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # document_id = str(uuid.uuid4())
        # Create Document record
    session = SessionLocal()
    try:
        document = Document(filename=filename)
        session.add(document)
        session.commit()
        session.refresh(document)  # populate the ID
        document_id = document.id
    except Exception as e:
        session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        session.close()

    celery_app.send_task('tasks.parse_file_task', args=[file_path, document_id])

    return jsonify({'message': 'File uploaded and sent for processing.', 'document_id': document_id}), 200

@app.route('/upload-url', methods=['POST'])
def upload_from_url():
    data = request.get_json()
    file_url = data.get('file_url')

    if not file_url:
        return jsonify({'error': 'Missing file_url'}), 400

    try:
        # Generate unique filename
        filename = f"{uuid.uuid4()}.pdf"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Download file from UploadThing to your server
        response = requests.get(file_url)
        with open(file_path, 'wb') as f:
            f.write(response.content)

        # Create Document record
        session = SessionLocal()
        document = Document(filename=filename)
        session.add(document)
        session.commit()
        session.refresh(document)
        document_id = document.id

    except Exception as e:
        session.rollback()
        return jsonify({'error': f'File download or DB error: {str(e)}'}), 500
    finally:
        session.close()

    # Kick off background task
    celery_app.send_task('tasks.parse_file_task', args=[file_path, document_id])

    return jsonify({'message': 'UploadThing file received & processing started.', 'document_id': document_id}), 200


@app.route('/slides', methods=['GET'])
def get_all_slides():
    session = SessionLocal()
    try:
        slides = session.query(Slide).all()
        result = [
            {
                'id': slide.id,
                'slide_number': slide.slide_number,
                'title': slide.title,
                'content': slide.content
            }
            for slide in slides
        ]
        return jsonify(result)
    finally:
        session.close()

@app.route('/slides/<document_id>', methods=['GET'])
def get_slides_by_document(document_id):
    session = SessionLocal()
    try:
        slides = session.query(Slide).filter(Slide.document_id == document_id).all()
        if not slides:
            return jsonify({'error': 'No slides found for this document_id'}), 404

        return jsonify([
            {
                'id': slide.id,
                'document_id': slide.document_id,
                'slide_number': slide.slide_number,
                'title': slide.title,
                'content': slide.content
            }
            for slide in slides
        ])
    finally:
        session.close()

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({'error': str(e)}), 500

# --- Run Server ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
