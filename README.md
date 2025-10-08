# Intranet Idea Submission Backend

This project implements the backend for an intranet idea submission form. It provides a RESTful API endpoint to receive, validate, and store new ideas submitted by employees.

## Features

- **RESTful API Endpoint:** `POST /api/ideas` for submitting new ideas.
- **Server-side Validation:** Ensures data integrity for idea `title`, `description`, `submitter_name`, and `submitter_email`.
- **Database Storage:** Persists submitted ideas into a central database (SQLite by default).
- **Error Handling & Logging:** Robust error handling and logging for API requests and database operations.
- **Extendable:** Designed for easy integration with existing intranet authentication mechanisms.

## Getting Started

### Prerequisites

- Python 3.9+
- `pip` (Python package installer)

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd intranet-idea-submission-backend
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

To run the FastAPI application, use Uvicorn:

```bash
uvicorn app.main:app --reload
```

This will start the server, typically accessible at `http://127.0.0.1:8000`.

### Database

The application uses a SQLite database named `ideas.db` by default, which will be created in the project root directory upon the first run. You can configure a different database by changing `SQLALCHEMY_DATABASE_URL` in `app/database.py`.

## API Reference

### `POST /api/ideas`

Submits a new idea.

#### Request Body

```json
{
  "title": "string",
  "description": "string",
  "submitter_name": "string",
  "submitter_email": "user@example.com"
}
```

**Fields:**

- `title` (string, required): The title of the idea. Minimum 1 character, maximum 255 characters.
- `description` (string, required): A detailed description of the idea. Minimum 1 character.
- `submitter_name` (string, required): The name of the idea submitter. Minimum 1 character, maximum 255 characters.
- `submitter_email` (string, required): The email address of the submitter. Must be a valid email format.

#### Responses

- **`201 Created`**: Idea submitted successfully.

  ```json
  {
    "message": "Idea submitted successfully!",
    "id": 1
  }
  ```

- **`422 Unprocessable Entity`**: Validation error due to invalid input.

  ```json
  {
    "detail": [
      {
        "loc": [
          "body",
          "title"
        ],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }
  ```

- **`500 Internal Server Error`**: An unexpected error occurred on the server.

  ```json
  {
    "detail": "Internal server error. Could not submit idea."
  }
  ```

## Development

### Authentication

For securing the API endpoint, integrate with your existing intranet authentication mechanisms. This might involve adding a dependency to `submit_idea` that validates an authentication token or session.

### Database Migrations

For managing database schema changes in a production environment, consider using a tool like Alembic.

## License

[Specify your license here, e.g., MIT, Apache 2.0]
