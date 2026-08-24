# Team Task Management Tool
A tool for team members to create and assign tasks efficiently.

## Setup
1. Clone the repository:
   ```
   git clone <repository-url>
   cd team-task-management-tool
   ```
2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python asep/api/main.py
   ```

## API Endpoints

### Create Task
- **Method:** POST
- **Path:** /api/tasks/
- **Request Body:**
  ```json
  {
    "title": "string",
    "description": "string",
    "assignee_id": "UUID"
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": "UUID",
    "title": "string",
    "description": "string",
    "status": "string",
    "assignee_id": "UUID",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST http://localhost:8000/api/tasks/ -H "Content-Type: application/json" -d '{"title": "Sample Task", "description": "This is a sample task", "assignee_id": "123e4567-e89b-12d3-a456-426614174000"}'
  ```

### List Tasks
- **Method:** GET
- **Path:** /api/tasks/
- **Response Shape:**
  ```json
  [
    {
      "id": "UUID",
      "title": "string",
      "description": "string",
      "status": "string",
      "assignee_id": "UUID",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ]
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/api/tasks/
  ```

### Read Task
- **Method:** GET
- **Path:** /api/tasks/{task_id}
- **Response Shape:**
  ```json
  {
    "id": "UUID",
    "title": "string",
    "description": "string",
    "status": "string",
    "assignee_id": "UUID",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/api/tasks/123e4567-e89b-12d3-a456-426614174000
  ```

### Assign Task
- **Method:** POST
- **Path:** /api/tasks/{task_id}/assign/
- **Request Body:**
  ```json
  {
    "assignee_id": "UUID"
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": "UUID",
    "title": "string",
    "description": "string",
    "status": "string",
    "assignee_id": "UUID",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST http://localhost:8000/api/tasks/123e4567-e89b-12d3-a456-426614174000/assign/ -H "Content-Type: application/json" -d '{"assignee_id": "123e4567-e89b-12d3-a456-426614174001"}'
  ```

### Get User Tasks
- **Method:** GET
- **Path:** /api/tasks/user/{user_id}
- **Response Shape:**
  ```json
  [
    {
      "id": "UUID",
      "title": "string",
      "description": "string",
      "status": "string",
      "assignee_id": "UUID",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ]
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/api/tasks/user/123e4567-e89b-12d3-a456-426614174001
  ```

### Update Task
- **Method:** PUT
- **Path:** /api/tasks/{task_id}
- **Request Body:**
  ```json
  {
    "title": "string",
    "description": "string",
    "status": "string",
    "assignee_id": "UUID"
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": "UUID",
    "title": "string",
    "description": "string",
    "status": "string",
    "assignee_id": "UUID",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```
- **Curl Example:**
  ```
  curl -X PUT http://localhost:8000/api/tasks/123e4567-e89b-12d3-a456-426614174000 -H "Content-Type: application/json" -d '{"title": "Updated Task", "description": "Updated description", "status": "in_progress", "assignee_id": "123e4567-e89b-12d3-a456-426614174001"}'
  ```

### Delete Task
- **Method:** DELETE
- **Path:** /api/tasks/{task_id}
- **Response Shape:**
  ```json
  {
    "detail": "Task deleted successfully"
  }
  ```
- **Curl Example:**
  ```
  curl -X DELETE http://localhost:8000/api/tasks/123e4567-e89b-12d3-a456-426614174000
  ```

## Models

### Task
- **Fields:**
  - id: UUID
  - title: string
  - description: string
  - status: string
  - assignee_id: UUID
  - created_at: datetime
  - updated_at: datetime

## Existing Sections
# asep-test-playground
Testing playground for ASEP application
