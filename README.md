# Habit Tracker
A web application for individuals to track their habits, monitor progress, and maintain consistency.

## Setup
1. Clone the repository:
   ```
   git clone <repository-url>
   cd habit-tracker
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
  curl -X POST http://localhost:8000/signup -H "Content-Type: application/json" -d '{"username": "testuser", "password": "password123"}'
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
    "id": "integer",
    "username": "string"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST http://localhost:8000/login -H "Content-Type: application/json" -d '{"username": "testuser", "password": "password123"}'
  ```

### Get User
- **Method:** GET
- **Path:** /users/{user_id}
- **Response Shape:**
  ```json
  {
    "id": "integer",
    "username": "string"
  }
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/users/1
  ```

### Delete User
- **Method:** DELETE
- **Path:** /users/{user_id}
- **Response Shape:**
  ```json
  {
    "detail": "User deleted successfully"
  }
  ```
- **Curl Example:**
  ```
  curl -X DELETE http://localhost:8000/users/1
  ```

### Update User
- **Method:** PUT
- **Path:** /users/{user_id}
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
  curl -X PUT http://localhost:8000/users/1 -H "Content-Type: application/json" -d '{"username": "newuser", "password": "newpassword"}'
  ```

### Create Habit
- **Method:** POST
- **Path:** /habits
- **Request Body:**
  ```json
  {
    "name": "string",
    "target_frequency": "string"  // e.g., "daily", "weekly"
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": "integer",
    "name": "string",
    "target_frequency": "string"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST http://localhost:8000/habits -H "Content-Type: application/json" -d '{"name": "Exercise", "target_frequency": "daily"}'
  ```

### Daily Check-in
- **Method:** POST
- **Path:** /habits/{habit_id}/checkin
- **Response Shape:**
  ```json
  {
    "habit_id": "integer",
    "date": "string",
    "streak": "integer",
    "longest_streak": "integer"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST http://localhost:8000/habits/1/checkin
  ```

### Weekly Progress
- **Method:** GET
- **Path:** /habits/{user_id}/weekly_progress
- **Response Shape:**
  ```json
  [
    {
      "habit_name": "string",
      "completion_rate": "float"
    }
  ]
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/habits/1/weekly_progress
  ```

## Models

### User
- **Fields:**
  - id: integer
  - username: string

### Habit
- **Fields:**
  - id: integer
  - name: string
  - target_frequency: string

### CheckIn
- **Fields:**
  - id: integer
  - habit_id: integer
  - date: string
  - streak: integer

## Existing Sections
# asep-test-playground
Testing playground for ASEP application
