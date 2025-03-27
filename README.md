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
DB_URL=
REDIS_URL=redis://<your-upstash-redis-url> (For production)
```

> Use the same Redis URL in both `api_gateway` and `parser_service`.

---

### Run with Docker Compose (Local)

```bash
# Build and run all services
docker-compose up --build
```

Services:

- API Gateway → http://localhost:5000
- Parser Service →
- PostgreSQL → localhost:5432
- Redis (via Upstash)

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

### 2. **List Parsed Decks**

**Endpoint:** `GET /slides`

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

**Endpoint:** `GET /slides/<id>`

**Description:** Returns slides and extracted content of a single deck.

---

## 🚀 Deployment on Render

### Strategy

Each service is deployed independently using Render’s **Docker** deployment method.

1. Push each service (e.g., `api_gateway`, `parser_service`) to one GitHub repo.
2. Set environment variables in the Render dashboard.

---

## Notes for  me... lol
<!--  -->

### 🛠 Option 1: Drop the table manually in Postgres
Open a terminal into your database container:
docker exec -it pitch-deck-parser-db-1 psql -U user -d pitchdeck
DROP TABLE slides;

## run docker

docker compose down
docker compose up --build

## To quickly visualize the top two levels of your folder structure.
tree -L 2
<!--  -->
````
