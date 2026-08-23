# Team Task Manager
A lightweight web application for small teams to track tasks and manage team collaboration.

## Setup
1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   uvicorn api.main:app --reload
   ```

## API Endpoints

### User Signup
- **Method:** POST
- **Path:** /signup
- **Request Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": "integer",
    "username": "string"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST "http://localhost:8000/signup" -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass"}'
  ```

### User Login
- **Method:** POST
- **Path:** /login
- **Request Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response Shape:**
  ```json
  {
    "message": "Login successful"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST "http://localhost:8000/login" -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass"}'
  ```

### Create Team
- **Method:** POST
- **Path:** /teams
- **Request Body:**
  ```json
  {
    "name": "string"
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": "integer",
    "name": "string"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST "http://localhost:8000/teams" -H "Content-Type: application/json" -d '{"name": "Team Alpha"}'
  ```

### Invite Team Member
- **Method:** POST
- **Path:** /teams/{team_id}/invite
- **Request Body:**
  ```json
  {
    "username": "string"
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": "integer",
    "name": "string"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST "http://localhost:8000/teams/1/invite" -H "Content-Type: application/json" -d '{"username": "newmember"}'
  ```

### Get Team
- **Method:** GET
- **Path:** /teams/{team_id}
- **Response Shape:**
  ```json
  {
    "id": "integer",
    "name": "string"
  }
  ```
- **Curl Example:**
  ```
  curl -X GET "http://localhost:8000/teams/1"
  ```

### Get Team Members
- **Method:** GET
- **Path:** /teams/{team_id}/members
- **Response Shape:**
  ```json
  [
    "string"
  ]
  ```
- **Curl Example:**
  ```
  curl -X GET "http://localhost:8000/teams/1/members"
  ```

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
  ```
  curl -X POST "http://localhost:8000/api/v1/tasks" -H "Content-Type: application/json" -d '{"title": "Test Task", "description": "This is a test task.", "assignee_id": 1}'
  ```

### Get Task
- **Method:** GET
- **Path:** /api/v1/tasks/{task_id}
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
  ```
  curl -X GET "http://localhost:8000/api/v1/tasks/1"
  ```

### Get All Tasks
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
  ```
  curl -X GET "http://localhost:8000/api/v1/tasks"
  ```

### Update Task
- **Method:** PUT
- **Path:** /api/v1/tasks/{task_id}
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
  ```
  curl -X PUT "http://localhost:8000/api/v1/tasks/1" -H "Content-Type: application/json" -d '{"title": "Updated Task", "description": "Updated description", "assignee_id": 1}'
  ```

### Delete Task
- **Method:** DELETE
- **Path:** /api/v1/tasks/{task_id}
- **Response Shape:**
  ```json
  {
    "detail": "Task deleted successfully"
  }
  ```
- **Curl Example:**
  ```
  curl -X DELETE "http://localhost:8000/api/v1/tasks/1"
  ```

### Create Activity Log
- **Method:** POST
- **Path:** /activity_logs
- **Request Body:**
  ```json
  {
    "task_id": "integer",
    "status": "string",
    "timestamp": "integer"
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": "integer",
    "task_id": "integer",
    "status": "string",
    "timestamp": "integer"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST "http://localhost:8000/activity_logs" -H "Content-Type: application/json" -d '{"task_id": 1, "status": "in-progress", "timestamp": 1633072800}'
  ```

### Get Activity Logs
- **Method:** GET
- **Path:** /activity_logs/{task_id}
- **Response Shape:**
  ```json
  [
    {
      "id": "integer",
      "task_id": "integer",
      "status": "string",
      "timestamp": "integer"
    }
  ]
  ```
- **Curl Example:**
  ```
  curl -X GET "http://localhost:8000/activity_logs/1"
  ```

## Models

### User
- **Fields:**
  - `id`: integer
  - `username`: string
  - `password`: string

### Team
- **Fields:**
  - `id`: integer
  - `name`: string

### Task
- **Fields:**
  - `id`: integer
  - `title`: string
  - `description`: string
  - `assignee_id`: integer
  - `status`: string
  - `created_at`: integer
  - `updated_at`: integer

### ActivityLog
- **Fields:**
  - `id`: integer
  - `task_id`: integer
  - `status`: string
  - `timestamp`: integer
