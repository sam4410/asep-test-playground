# Todo App

A simple shared todo list web app with a FastAPI backend and a Next.js frontend. Users can create tasks, mark them complete, and delete them. No authentication is used.

## Setup

### Backend

1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set the database URL to a PostgreSQL database:
   ```bash
   export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/todos"
   ```
4. Run the API:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend

1. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the Next.js app:
   ```bash
   npm run dev
   ```

### Database

Apply the Alembic migration to create the `todos` table:
```bash
alembic upgrade head
```

## API Endpoints

### GET /health

Returns the service health status.

- Request body: none
- Response shape:
  - `status` (string)

Example:
```bash
curl http://localhost:8000/health
```

### GET /api/v1/todos

Lists all todos.

- Request body: none
- Response shape: array of todo objects

Example:
```bash
curl http://localhost:8000/api/v1/todos
```

### POST /api/v1/todos

Creates a new todo.

- Request body:
  - `title` (string, required, max 500 chars, trimmed, must not be blank)
- Response shape: todo object

Example:
```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Write tests"}'
```

### PATCH /api/v1/todos/{todo_id}

Updates a todo.

- Request body:
  - `title` (string, optional, max 500 chars, trimmed, must not be blank if provided)
  - `completed` (boolean, optional)
- Response shape: todo object

Example:
```bash
curl -X PATCH http://localhost:8000/api/v1/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'
```

### DELETE /api/v1/todos/{todo_id}

Deletes a todo.

- Request body: none
- Response shape: no content (`204`)

Example:
```bash
curl -X DELETE http://localhost:8000/api/v1/todos/1
```

## Models

### Todo database model

Fields:

- `id` (integer, primary key)
- `title` (string, required, max 500 chars)
- `completed` (boolean, required, default `false`)
- `created_at` (datetime with timezone, required)
- `updated_at` (datetime with timezone, required)

Constraints and indexes:

- Title must not be blank
- Index on `created_at`
- Index on `(completed, created_at)`

### API schemas

#### TodoCreate

- `title` (string, required, max 500 chars, trimmed, must not be blank)

#### TodoUpdate

- `title` (string, optional, max 500 chars, trimmed, must not be blank if provided)
- `completed` (boolean, optional)

#### TodoResponse

- `id` (integer)
- `title` (string)
- `completed` (boolean)
- `created_at` (datetime)
- `updated_at` (datetime)

## Frontend

The Next.js app is configured to proxy `/api/v1/*` requests to the backend. The frontend API client uses the same route shape as the backend, so it can call the API through the browser or directly against the FastAPI server.
