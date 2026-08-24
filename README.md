# Team Task Manager
A lightweight web application for small teams to track tasks and manage work without the overhead of a full project-management suite.

## Setup
1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <project-directory>`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up the database: Follow the instructions in the database setup documentation.
5. Run the application: `python app.py` (or the appropriate command for your setup).

## API Endpoints

### User Signup
- **Method:** POST
- **Path:** /api/auth/signup
- **Request Body:**
  ```json
  {
    "username": "string",
    "password": "string",
    "email": "string"
  }
  ```
- **Response Shape:**
  ```json
  {
    "message": "User created successfully",
    "user_id": "string"
  }
  ```
- **Curl Example:**
  ```bash
  curl -X POST http://localhost:5000/api/auth/signup -H "Content-Type: application/json" -d '{"username": "testuser", "password": "password123", "email": "test@example.com"}'
  ```

### User Login
- **Method:** POST
- **Path:** /api/auth/login
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
    "message": "Login successful",
    "token": "string"
  }
  ```
- **Curl Example:**
  ```bash
  curl -X POST http://localhost:5000/api/auth/login -H "Content-Type: application/json" -d '{"username": "testuser", "password": "password123"}'
  ```

### Create Task
- **Method:** POST
- **Path:** /api/tasks
- **Request Body:**
  ```json
  {
    "title": "string",
    "description": "string",
    "assignee": "string",
    "due_date": "string",
    "status": "string" // "todo", "in-progress", "done"
  }
  ```
- **Response Shape:**
  ```json
  {
    "message": "Task created successfully",
    "task_id": "string"
  }
  ```
- **Curl Example:**
  ```bash
  curl -X POST http://localhost:5000/api/tasks -H "Content-Type: application/json" -d '{"title": "New Task", "description": "Task description", "assignee": "testuser", "due_date": "2023-12-31", "status": "todo"}'
  ```

### Get Tasks
- **Method:** GET
- **Path:** /api/tasks
- **Response Shape:**
  ```json
  [
    {
      "task_id": "string",
      "title": "string",
      "description": "string",
      "assignee": "string",
      "due_date": "string",
      "status": "string"
    }
  ]
  ```
- **Curl Example:**
  ```bash
  curl -X GET http://localhost:5000/api/tasks
  ```

## Models

### User
- `user_id`: string
- `username`: string
- `password`: string
- `email`: string

### Task
- `task_id`: string
- `title`: string
- `description`: string
- `assignee`: string
- `due_date`: string
- `status`: string (values: "todo", "in-progress", "done")

## Existing Sections
# asep-test-playground
Testing playground for ASEP application
