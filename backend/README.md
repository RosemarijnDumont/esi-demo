
# Financial Export Backend Service

This service provides an API for asynchronously exporting financial transaction data. It is designed to handle large datasets by implementing data chunking/pagination, asynchronous processing with Celery, and utilizing a read-replica database to offload the primary database.

## Features

*   **Asynchronous Export**: Long-running export tasks are offloaded to Celery workers, preventing API timeouts.
*   **Data Chunking**: Financial data is retrieved from the database in batches to reduce memory usage and prevent database timeouts.
*   **Read-Replica Support**: Configurable to use a dedicated read-replica for export queries, minimizing impact on the primary operational database.
*   **Optimized SQL**: Database queries are designed to be efficient, leveraging date-range indexes.
*   **Caching**: `lru_cache` is used for frequently accessed, static reference data (e.g., transaction categories).
*   **FastAPI**: Provides a modern, high-performance web API.
*   **Dockerized**: Easy to deploy using Docker.

## Architecture Overview

*   **FastAPI**: Exposes REST endpoints to trigger and monitor export tasks.
*   **Celery**: A distributed task queue that handles the actual data export process in background workers.
*   **Redis**: Used as both Celery broker and result backend.
*   **PostgreSQL**: The primary database storing financial transaction data.
*   **PostgreSQL Read-Replica (Optional)**: A separate database instance optimized for read operations, used by the export service.

```mermaid
graph TD
    A[Client] -->|HTTP POST /export| B(FastAPI)
    B -->|Enqueues Task| C(Celery Broker - Redis)
    C -->|Sends Task to| D(Celery Worker)
    D -->|Calls| E(FinancialExportService)
    E -->|Fetches data in chunks from| F{Read-Replica DB}
    F -->|Returns data| E
    E -->|Processes & Exports to| G(CSV File on Disk)
    D -->|Updates Task Status| H(Celery Result Backend - Redis)
    A -->|HTTP GET /export/status/{task_id}| B
    B -->|Retrieves Status from| H
```

## Getting Started

### Prerequisites

*   Docker and Docker Compose
*   Python 3.10+
*   A PostgreSQL database (and optionally, a read replica)
*   Redis (for Celery)

### Setup

1.  **Clone the repository:**

    ```bash
    git clone <your-repo-url>
    cd financial-export-backend
    ```

2.  **Configure environment variables:**

    Create a `.env` file in the `backend/` directory by copying from `.env.example` and filling in your database and Redis connection details.

    ```bash
    cp backend/.env.example backend/.env
    # Edit backend/.env with your actual configurations
    ```

    **Example `.env` content:**

    ```dotenv
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    DATABASE_NAME=financial_db
    DATABASE_USER=admin
    DATABASE_PASSWORD=secret
    DB_STATEMENT_TIMEOUT_MS=300000

    # Uncomment and configure if using a read replica
    # READ_REPLICA_HOST=localhost
    # READ_REPLICA_NAME=financial_db
    # READ_REPLICA_USER=reader
    # READ_REPLICA_PASSWORD=readonly_secret

    CELERY_BROKER_URL=redis://localhost:6379/0
    CELERY_RESULT_BACKEND=redis://localhost:6379/0

    EXPORT_BATCH_SIZE=50000
    EXPORT_FILE_DIR=/app/exports
    ```

3.  **Database Setup:**

    Ensure your PostgreSQL database is running and accessible. You'll need tables like `financial_transactions` and `transaction_categories`. Here's example SQL for table creation and indexing:

    ```sql
    -- financial_transactions table
    CREATE TABLE financial_transactions (
        id SERIAL PRIMARY KEY,
        transaction_date TIMESTAMP WITH TIME ZONE NOT NULL,
        amount NUMERIC(15, 2) NOT NULL,
        currency VARCHAR(3) NOT NULL,
        description VARCHAR(500),
        category_id INTEGER, -- Foreign key to transaction_categories
        account_id INTEGER NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        metadata JSONB
    );

    -- Indexes for efficient querying
    CREATE INDEX idx_financial_transactions_date ON financial_transactions (transaction_date);
    CREATE INDEX idx_financial_transactions_category_id ON financial_transactions (category_id);
    CREATE INDEX idx_financial_transactions_account_id ON financial_transactions (account_id);

    -- transaction_categories table (for caching example)
    CREATE TABLE transaction_categories (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE
    );

    -- Add some sample categories
    INSERT INTO transaction_categories (name) VALUES ('Income'), ('Groceries'), ('Utilities'), ('Rent'), ('Salary');

    -- Add a foreign key constraint (optional, but good practice)
    ALTER TABLE financial_transactions
    ADD CONSTRAINT fk_category
    FOREIGN KEY (category_id)
    REFERENCES transaction_categories (id);

    -- Sample Data (Optional)
    INSERT INTO financial_transactions (transaction_date, amount, currency, description, category_id, account_id)
    SELECT
        '2023-01-01'::date + (floor(random() * 364) || ' days')::interval + (floor(random() * 24) || ' hours')::interval + (floor(random() * 60) || ' minutes')::interval,
        (random() * 1000 + 10)::numeric(15, 2),
        CASE WHEN random() < 0.5 THEN 'USD' ELSE 'EUR' END,
        'Transaction ' || generate_series(1, 100000),
        (floor(random() * 5) + 1)::int,
        (floor(random() * 3) + 1)::int
    FROM generate_series(1, 100000);
    ```

4.  **Build and run with Docker Compose:**

    ```bash
    docker-compose -f docker-compose.yaml up --build
    ```

    This will start:
    *   The FastAPI application (`backend` service)
    *   A Celery worker (`celery_worker` service)
    *   A Redis instance (`redis` service)

    You can access the FastAPI application at `http://localhost:8000` (or the port you configured).

## API Endpoints

### 1. Trigger Financial Export

Initiates an asynchronous export process for a specified quarter and year.

*   **Endpoint**: `POST /export`
*   **Query Parameters**:
    *   `quarter`: `str` (e.g., "Q1", "Q2", "Q3", "Q4")
    *   `year`: `int` (e.g., 2023)
*   **Response**: `202 Accepted` with a `task_id`.

**Example Request (using `curl`):**

```bash
curl -X POST "http://localhost:8000/export?quarter=Q1&year=2023"
```

**Example Response:**

```json
{
  "task_id": "b3f4e1a2-c5d6-4e7f-8a9b-1c0d2e3f4a5b",
  "status": "Export process initiated",
  "message": "You can check the status of the export using the /export/status/{task_id} endpoint."
}
```

### 2. Get Export Status

Retrieves the current status of an export task using its `task_id`.

*   **Endpoint**: `GET /export/status/{task_id}`
*   **Path Parameter**:
    *   `task_id`: `str` (the ID received from the `/export` endpoint)
*   **Response**: `200 OK` with task status, message, and potentially results.

**Example Request:**

```bash
curl "http://localhost:8000/export/status/b3f4e1a2-c5d6-4e7f-8a9b-1c0d2e3f4a5b"
```

**Example Response (in progress):**

```json
{
  "status": "STARTED",
  "message": "Export is in progress."
}
```

**Example Response (completed):**

```json
{
  "status": "SUCCESS",
  "message": "Export completed successfully.",
  "result": {
    "status": "completed",
    "file_path": "/app/exports/financial_export_2023_Q1_20231120153000.csv",
    "duration": 15.67
  }
}
```

**Example Response (failed):**

```json
{
  "status": "FAILURE",
  "message": "Export failed.",
  "error": "NameOfError: Details of the error"
}
```

## Development

### Running Locally (without Docker Compose)

1.  **Install dependencies:**

    ```bash
    pip install -r backend/requirements.txt
    ```

2.  **Ensure Redis is running** (e.g., `redis-server`).

3.  **Run FastAPI application:**

    ```bash
    cd backend
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

4.  **Run Celery worker:**

    Open a new terminal and navigate to the `backend` directory:

    ```bash
    celery -A app.core.celery_app worker --loglevel=info -P gevent
    ```
    (The `-P gevent` is recommended for I/O bound tasks, ensure `gevent` is in `requirements.txt` if used)

### SQL Indexing

Ensure the following indexes are applied to your `financial_transactions` table to optimize query performance:

```sql
CREATE INDEX idx_financial_transactions_date ON financial_transactions (transaction_date);
CREATE INDEX idx_financial_transactions_category_id ON financial_transactions (category_id);
-- Add other relevant indexes as needed, e.g., on account_id if frequently filtered
```

### `DB_STATEMENT_TIMEOUT_MS`

This setting in `.env` controls how long a single database statement is allowed to run before timing out. It's crucial for long-running queries in export processes. Adjust as necessary based on your data volume and database performance.

## Troubleshooting

*   **Celery tasks not starting**: Check if the Celery worker is running and connected to the Redis broker. Look for error messages in the worker's console output.
*   **Database timeouts**: Increase `DB_STATEMENT_TIMEOUT_MS` in your `.env` file and ensure your database has appropriate indexes on `transaction_date` and other frequently queried columns.
*   **"Task not found"**: Ensure the `task_id` is correct and that the Celery result backend (Redis) is properly configured and accessible.
*   **File export issues**: Check the `EXPORT_FILE_DIR` setting to ensure the directory exists and the application has write permissions. Inside Docker, `EXPORT_FILE_DIR` should be a path within the container like `/app/exports`.

