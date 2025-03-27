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
