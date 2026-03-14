# TaskForge – Distributed Task Processing System

TaskForge is a lightweight distributed task processing system built with Python.
It allows applications to submit background jobs that are processed asynchronously by worker processes.

The system uses a queue-based architecture with Redis and PostgreSQL to ensure reliable task execution, retry handling, and task status tracking.

TaskForge demonstrates core backend engineering concepts such as asynchronous processing, distributed workers, message queues, and fault tolerance.

---

## Architecture Overview

TaskForge follows a producer–consumer architecture.

```
Client
  |
  |  HTTP Request
  v
FastAPI (API Service)
  |
  |  Push task ID
  v
Redis Queue
  |
  |  Worker pulls task
  v
Worker Service
  |
  |  Execute task
  v
PostgreSQL (task state + result)
```

### Components

**API Service**

* Built with FastAPI
* Accepts task submissions
* Stores task metadata in PostgreSQL
* Pushes task IDs into Redis queue

**Worker Service**

* Independent Python process
* Pulls tasks from Redis
* Executes task handlers
* Updates task status and result

**Redis**

* Acts as the message broker
* Manages task queues

**PostgreSQL**

* Stores task metadata
* Tracks task lifecycle and results

---

## Key Features

* Asynchronous task execution
* Redis-based message queue
* Distributed worker support
* Retry mechanism for failed tasks
* Crash recovery using processing queues
* Task status tracking via API
* Docker-based infrastructure setup

---

## Task Lifecycle

Each task transitions through the following states:

```
PENDING  → task created
RUNNING  → worker processing task
SUCCESS  → completed successfully
FAILED   → failed after retries
```

Retry logic:

```
RUNNING → FAILED → RETRY → RUNNING
```

Maximum retry attempts are configurable.

---

## Project Structure

```
taskforge/
│
├── docker-compose.yml
├── README.md
├── .env.example
├── .gitignore
│
├── api/
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── database.py
│       ├── models.py
│       ├── schemas.py
│       ├── routes/
│       │   └── tasks.py
│       └── services/
│           └── task_service.py
│
└── worker/
    ├── requirements.txt
    ├── worker.py
    ├── database.py
    ├── models.py
    ├── redis_client.py
    └── task_handlers.py
```

---

## Setup Instructions

### 1. Clone Repository

```
git clone https://github.com/YOUR_USERNAME/taskforge.git
cd taskforge
```

---

### 2. Create Environment File

```
cp .env.example .env
```

Example `.env` configuration:

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/taskforge
REDIS_URL=redis://localhost:6379/0
```

---

### 3. Start Infrastructure

Start Redis and PostgreSQL using Docker.

```
docker compose up -d
```

This will start:

* PostgreSQL
* Redis

---

### 4. Run API Service

```
cd api

python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt

uvicorn app.main:app --reload
```

API will run at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

### 5. Run Worker

Open a new terminal:

```
cd worker

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python worker.py
```

The worker will start consuming tasks from Redis.

---
## Example Usage

### Create Task

```
POST /tasks
```

Example request body:

```json
{
  "type": "sleep",
  "payload": {
    "duration": 5
  }
}
```

Response:

```json
{
  "id": "task_id",
  "status": "PENDING",
  "result": null
}
```

---

### Check Task Status

```
GET /tasks/{task_id}
```

Response example:

```json
{
  "id": "task_id",
  "status": "SUCCESS",
  "result": {
    "message": "Slept for 5 seconds"
  }
}
```

---

## Supported Task Types

Example handlers implemented:

* `sleep` – simulate background processing
* `math` – perform simple arithmetic operations

New tasks can be added by extending the `TASK_HANDLERS` dictionary in:

```
worker/task_handlers.py
```

---

## Reliability Features

TaskForge includes mechanisms to improve reliability.

**Processing Queue**

Tasks are moved from:

```
task_queue → processing_queue
```

This ensures tasks are not lost if a worker crashes during execution.

**Crash Recovery**

On worker startup:

* Any tasks stuck in `processing_queue`
* Are automatically returned to the main queue.

**Retry Mechanism**

Failed tasks are retried up to a maximum retry limit.

---

## Scaling Workers

Multiple workers can run concurrently.

Example:

```
python worker.py
python worker.py
python worker.py
```

Redis ensures tasks are distributed across workers.

---

## Technologies Used

* Python
* FastAPI
* SQLAlchemy (async)
* PostgreSQL
* Redis
* Docker
* Pydantic

---

## Future Improvements

Potential enhancements include:

* task scheduling
* priority queues
* monitoring dashboard
* rate limiting
* distributed tracing
* task timeouts
* dead letter queue

---

## Learning Objectives

This project demonstrates important backend engineering concepts:

* asynchronous processing
* distributed worker architecture
* queue-based systems
* retry and failure handling
* service separation
* infrastructure management

---

## License

MIT License
