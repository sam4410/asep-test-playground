# Habit Tracker - A mobile app for tracking daily habits

This repository contains a complete React Native/Expo mobile application with a FastAPI backend designed to help young professionals build daily habits by tracking streaks with a one-tap check-in.

## Setup

### Backend
1. Navigate to the `backend` directory.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

### Frontend
1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```
   npm install
   ```
3. Start the Expo application:
   ```
   expo start
   ```

## API Endpoints

### Authentication
- **POST /auth/signup**
  - Request Body:
    ```json
    {
      "username": "string",
      "email": "string",
      "password": "string"
    }
    ```
  - Response:
    ```json
    {
      "access_token": "string",
      "token_type": "string"
    }
    ```
  - Example:
    ```
    curl -X POST "http://localhost:8000/auth/signup" -H "Content-Type: application/json" -d '{"username": "testuser", "email": "test@example.com", "password": "testpassword"}'
    ```

- **POST /auth/login**
  - Request Body:
    ```json
    {
      "username": "string",
      "email": "string",
      "password": "string"
    }
    ```
  - Response:
    ```json
    {
      "access_token": "string",
      "token_type": "string"
    }
    ```
  - Example:
    ```
    curl -X POST "http://localhost:8000/auth/login" -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}'
    ```

### Habits
- **POST /habits/**
  - Request Body:
    ```json
    {
      "name": "string"
    }
    ```
  - Response:
    ```json
    {
      "id": "integer",
      "user_id": "integer",
      "name": "string",
      "streak": "integer",
      "created_at": "string"
    }
    ```
  - Example:
    ```
    curl -X POST "http://localhost:8000/habits/" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"name": "Read a book"}'
    ```

- **GET /habits/**
  - Response:
    ```json
    [
      {
        "id": "integer",
        "user_id": "integer",
        "name": "string",
        "streak": "integer",
        "created_at": "string"
      }
    ]
    ```
  - Example:
    ```
    curl -X GET "http://localhost:8000/habits/" -H "Authorization: Bearer <token>"
    ```

- **GET /habits/{habit_id}**
  - Response:
    ```json
    {
      "id": "integer",
      "user_id": "integer",
      "name": "string",
      "streak": "integer",
      "created_at": "string"
    }
    ```
  - Example:
    ```
    curl -X GET "http://localhost:8000/habits/1" -H "Authorization: Bearer <token>"
    ```

- **PUT /habits/{habit_id}**
  - Request Body:
    ```json
    {
      "name": "string"
    }
    ```
  - Response:
    ```json
    {
      "id": "integer",
      "user_id": "integer",
      "name": "string",
      "streak": "integer",
      "created_at": "string"
    }
    ```
  - Example:
    ```
    curl -X PUT "http://localhost:8000/habits/1" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"name": "Updated Habit"}'
    ```

- **DELETE /habits/{habit_id}**
  - Response:
    ```json
    {
      "message": "Habit deleted successfully"
    }
    ```
  - Example:
    ```
    curl -X DELETE "http://localhost:8000/habits/1" -H "Authorization: Bearer <token>"
    ```

## Models

### User
- `id`: integer
- `username`: string
- `email`: string
- `hashed_password`: string
- `created_at`: string (ISO 8601 format)

### Habit
- `id`: integer
- `user_id`: integer
- `name`: string
- `streak`: integer
- `created_at`: string (ISO 8601 format)
