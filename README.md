# Note Taking API
A simple note-taking API that allows users to create notes with a title and body, storing them in a database.

## Setup
1. Clone the repository.
2. Navigate to the project directory.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```
   alembic upgrade head
   ```
5. Start the API:
   ```
   python asep/api/main.py
   ```

## API Endpoints

### POST /api/v1/notes
- **Request Body:**
  ```json
  {
    "title": "string",
    "body": "string"
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": "integer",
    "title": "string",
    "body": "string",
    "created_at": "string (ISO 8601 format)"
  }
  ```
- **Curl Example:**
  ```bash
  curl -X POST "http://localhost:8000/api/v1/notes" -H "Content-Type: application/json" -d '{"title": "Test Note", "body": "This is a test note."}'
  ```

## Models
### Note
- **id**: Integer, primary key, auto-incremented
- **title**: String, required
- **body**: String, required
- **created_at**: DateTime, defaults to current UTC time

## Existing README
# asep-test-playground
Testing playground for ASEP application
