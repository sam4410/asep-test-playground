# Habit Tracker App
A simple web application for tracking daily habits and monitoring streaks.

## Setup
1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <project-directory>`
3. Install dependencies: `pip install -r requirements.txt`
4. Run database migrations: `alembic upgrade head`
5. Start the application: `uvicorn api.main:app --reload`

## API Endpoints

### Log Habit
- **Method:** POST
- **Path:** /habits/log
- **Request Body:**
```json
{
    "habit_name": "string",
    "user_id": "integer"
}
```
- **Response Shape:**
```json
{
    "id": "integer",
    "name": "string",
    "streak_count": "integer",
    "user_id": "integer"
}
```
- **Curl Example:**
```bash
curl -X POST http://localhost:8000/habits/log -H "Content-Type: application/json" -d '{"habit_name": "Test Habit", "user_id": 1}'
```

### Create Habit
- **Method:** POST
- **Path:** /habits
- **Request Body:**
```json
{
    "name": "string",
    "target_frequency": "integer"
}
```
- **Response Shape:**
```json
{
    "id": "integer",
    "name": "string",
    "target_frequency": "integer"
}
```
- **Curl Example:**
```bash
curl -X POST http://localhost:8000/habits -H "Content-Type: application/json" -d '{"name": "Test Habit", "target_frequency": 1}'
```

### Get Habits
- **Method:** GET
- **Path:** /habits
- **Request Query Parameters:** 
  - `user_id`: integer
- **Response Shape:**
```json
[
    {
        "id": "integer",
        "name": "string",
        "streak_count": "integer"
    }
]
```
- **Curl Example:**
```bash
curl -X GET "http://localhost:8000/habits?user_id=1"
```

### Get Habit
- **Method:** GET
- **Path:** /habits/{habit_id}
- **Response Shape:**
```json
{
    "id": "integer",
    "name": "string",
    "streak_count": "integer"
}
```
- **Curl Example:**
```bash
curl -X GET http://localhost:8000/habits/1
```

### Get Habit Streak
- **Method:** GET
- **Path:** /habits/streak/{habit_id}
- **Response Shape:**
```json
{
    "habit_id": "integer",
    "streak_count": "integer"
}
```
- **Curl Example:**
```bash
curl -X GET http://localhost:8000/habits/streak/1
```

## Models
### Habit
- **id**: Integer, primary key
- **name**: String, not nullable
- **streak_count**: Integer, default 0
- **user_id**: Integer, foreign key to users, not nullable

## Existing Sections
### Small Online Store
A simple web application for a small business to manage an online storefront, including product catalog, shopping cart, and checkout functionality.
