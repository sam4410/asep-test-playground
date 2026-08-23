# Team Task Management Tool
A tool for team members to create and assign tasks efficiently.

## Setup
1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <project-directory>`
3. Install dependencies: `pip install -r requirements.txt`
4. Run database migrations: `alembic upgrade head`
5. Start the application: `uvicorn api.main:app --reload`

## API Endpoints

### Create Task
- **Method:** POST
- **Path:** /api/v1/tasks
- **Request Body:**
```json
{
    "title": "string",
    "description": "string",
    "assignee_id": "integer"
}
```
- **Response Shape:**
```json
{
    "id": "integer",
    "title": "string",
    "description": "string",
    "assignee_id": "integer",
    "status": "string",
    "created_at": "integer",
    "updated_at": "integer"
}
```
- **Curl Example:**
```bash
curl -X POST http://localhost:8000/api/v1/tasks -H "Content-Type: application/json" -d '{"title": "Test Task", "description": "This is a test task.", "assignee_id": 1}'
```

### Get Tasks
- **Method:** GET
- **Path:** /api/v1/tasks
- **Response Shape:**
```json
[
    {
        "id": "integer",
        "title": "string",
        "description": "string",
        "assignee_id": "integer",
        "status": "string",
        "created_at": "integer",
        "updated_at": "integer"
    }
]
```
- **Curl Example:**
```bash
curl -X GET http://localhost:8000/api/v1/tasks
```

## Models

### Task
- **id**: Integer, primary key
- **title**: String, task title
- **description**: String, task description
- **assignee_id**: Integer, foreign key to User
- **status**: String, task status (e.g., "todo", "in_progress", "done")
- **created_at**: Integer, timestamp for task creation
- **updated_at**: Integer, timestamp for last update

## Existing Sections
### Small Online Store
A simple web application for a small business to manage an online storefront, including product catalog, shopping cart, and checkout functionality.
