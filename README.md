# Habit Tracker App
A web application for users to log daily habits and track their streaks.

## Setup
1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <project-directory>`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up the database: Follow the instructions in the database setup documentation.
5. Run the application: `python asep/api/main.py` (or the appropriate command for your setup).

## API Endpoints

### Log Habit
- **Method:** POST
- **Path:** /api/habits/log
- **Request Body:**
  ```json
  {
    "user_id": "string",
    "habit_name": "string",
    "log_date": "string" (optional, ISO 8601 format)
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": "string",
    "user_id": "string",
    "habit_name": "string",
    "log_date": "string"
  }
  ```
- **Curl Example:**
  ```bash
  curl -X POST http://localhost:8000/api/habits/log -H "Content-Type: application/json" -d '{"user_id": "test_user", "habit_name": "Exercise", "log_date": "2023-10-01T00:00:00Z"}'
  ```

### Get Habits
- **Method:** GET
- **Path:** /api/habits/
- **Query Parameters:** `user_id` (string)
- **Response Shape:**
  ```json
  [
    {
      "id": "string",
      "user_id": "string",
      "habit_name": "string",
      "log_date": "string"
    }
  ]
  ```
- **Curl Example:**
  ```bash
  curl -X GET "http://localhost:8000/api/habits/?user_id=test_user"
  ```

## Models

### HabitModel
- `id`: UUID
- `user_id`: string
- `habit_name`: string
- `log_date`: datetime
- `streak_count`: integer

## Existing Sections
# asep-test-playground
Testing playground for ASEP application
