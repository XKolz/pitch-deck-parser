mkdir pitch-deck-parser
cd pitch-deck-parser

mkdir api parser db
touch docker-compose.yml

### 📁 README.md

# Pitch Deck Parser (Backend Assessment)

## Overview

Flask-based app to upload and parse pitch decks (PDF/PPTX), using Celery + Redis for background processing, and PostgreSQL for storage.

## How to Run

```bash
docker compose up --build
```

## Upload API

POST `/upload`

- Form-Data: `file` = .pdf or .pptx

Uploads the file, stores it locally, and queues a background parsing task.

## Tech Stack

- Flask
- Celery + Redis
- PostgreSQL
- Docker Compose

<!--  -->

Your system:

✅ Accepted a file via the Flask API
✅ Saved it to the uploads/ folder
✅ Sent the task to Celery via Redis
✅ Parsed the file (beautiful log from parser_service)
✅ Logged the extracted data correctly
✅ And no errors anywhere — chef’s kiss 👨‍🍳💻

### 🛠 Option 1: Drop the table manually in Postgres

Open a terminal into your database container:
docker exec -it pitch-deck-parser-db-1 psql -U user -d pitchdeck
DROP TABLE slides;

docker compose down
docker compose up --build

## To quickly visualize the top two levels of your folder structure.

tree -L 2

Got you! Here's a complete, professional `README.md` tailored for your Flask-based pitch deck parser project with Docker Compose, Render deployment, Redis (Upstash), and separate services:

---

````md
# Pitch Deck Parser API

A full-stack web application that parses pitch decks (PDF or PPTX), extracts slide data, and presents them on a dashboard. This project is composed of multiple backend services, including an API gateway, a document parser, Redis for task handling, and PostgreSQL or MongoDB for persistent storage.

---

## 🚀 Features

- Upload and parse pitch decks (PDF/PPTX)
- Extract slide content and metadata
- Store data in a relational or NoSQL database
- Background task processing with Celery and Redis
- REST API for accessing parsed data
- Dockerized microservices
- Ready for deployment on Render

---

## 🧱 Architecture

```bash
.
├── api_gateway/          # Flask API for handling client requests
├── parser_service/       # Document parser with Celery workers
├── database/             # DB initialization scripts and models
├── docker-compose.yml    # Compose configuration
└── README.md
```
````

---

## 🛠️ Setup Instructions

### Prerequisites

- Docker + Docker Compose
- Git
- Upstash Redis account (for Celery broker)
- Render account (for deployment)
- Python 3.10+ (for local development)

---

### ⚙️ Environment Variables

Create a `.env` file in the project root with:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=pitchdeck
REDIS_URL=redis://<your-upstash-redis-url>
PARSER_SERVICE_URL=http://parser_service:5001
```

> Use the same Redis URL in both `api_gateway` and `parser_service`.

---

### 🐳 Run with Docker Compose (Local)

```bash
# Build and run all services
docker-compose up --build
```

Services:

- API Gateway → http://localhost:5000
- Parser Service → http://localhost:5001
- PostgreSQL → localhost:5432
- Redis (via Upstash)

---

## 🧪 Running Tests

If you have test suites (e.g. Pytest), you can run:

```bash
docker exec -it api_gateway bash
pytest
```

Or run locally using your Python environment with:

```bash
cd api_gateway
pytest
```

---

## 📮 API Routes

### 1. **Upload Pitch Deck**

**Endpoint:** `POST /upload`

**Description:** Uploads a PDF or PPTX file and triggers the parsing task.

**Request:**

- `multipart/form-data`
- Field: `file` (PDF or PPTX)

**Response:**

```json
{
  "message": "Parsing started",
  "task_id": "abc123"
}
```

---

### 2. **Get Task Status**

**Endpoint:** `GET /status/<task_id>`

**Description:** Checks the status of a background parsing task.

**Response:**

```json
{
  "status": "PENDING" | "SUCCESS" | "FAILURE",
  "result": {...}  // if successful
}
```

---

### 3. **List Parsed Decks**

**Endpoint:** `GET /decks`

**Description:** Returns a list of parsed pitch decks with metadata.

**Response:**

```json
[
  {
    "id": 1,
    "filename": "startup_deck.pdf",
    "uploaded_at": "2025-03-27T10:00:00Z"
  }
]
```

---

### 4. **Get Deck Details**

**Endpoint:** `GET /decks/<id>`

**Description:** Returns slides and extracted content of a single deck.

---

## 🚀 Deployment on Render

### Strategy

Each service is deployed independently using Render’s **Docker** deployment method.

1. Push each service (e.g., `api_gateway`, `parser_service`) to a separate GitHub repo.
2. Connect each repo to a **Render Web Service**.
3. Configure build & start commands:

**Example for API Gateway:**

- **Dockerfile Path:** `/api_gateway/Dockerfile`
- **Build Command:** _Leave blank_
- **Start Command:** `gunicorn app:app -b 0.0.0.0:5000`

4. Set environment variables in the Render dashboard.

---

## 📎 Notes

- For production, ensure HTTPS and security configurations (rate limiting, input validation, etc.)
- You can switch between PostgreSQL and MongoDB by adjusting the parser and database models.

---

## 👨‍💻 Author

Samuel – Backend Specialist | Full-Stack Developer

---

## 📃 License

MIT License

```

---

Let me know if you want to customize this further for PostgreSQL vs MongoDB, Celery retries, or if you want to generate OpenAPI docs as well.
```
