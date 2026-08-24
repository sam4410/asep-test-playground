# Student Quiz Platform
A web application for teachers to create quizzes and track student performance without the complexity of a full learning-management system.

## Setup
1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <project-directory>`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up the database: Follow the instructions in the database setup documentation.
5. Run the application: `python api/main.py` (or the appropriate command for your setup).

## API Endpoints

### Create Quiz
- **Method:** POST
- **Path:** /quizzes/
- **Request Body:**
  ```json
  {
    "title": "string",
    "questions": []
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": "string",
    "title": "string",
    "teacher_id": "string",
    "created_at": "string",
    "questions": []
  }
  ```
- **Curl Example:**
  ```bash
  curl -X POST http://localhost:8000/quizzes/ -H "Content-Type: application/json" -d '{"title": "Sample Quiz", "questions": []}' --data-urlencode "teacher_id=some-teacher-id"
  ```

### Get Quiz by ID
- **Method:** GET
- **Path:** /quizzes/{quiz_id}
- **Response Shape:**
  ```json
  {
    "id": "string",
    "title": "string",
    "teacher_id": "string",
    "created_at": "string",
    "questions": []
  }
  ```
- **Curl Example:**
  ```bash
  curl -X GET http://localhost:8000/quizzes/some-quiz-id
  ```

### List Quizzes
- **Method:** GET
- **Path:** /quizzes/
- **Response Shape:**
  ```json
  [
    {
      "id": "string",
      "title": "string",
      "teacher_id": "string",
      "created_at": "string",
      "questions": []
    }
  ]
  ```
- **Curl Example:**
  ```bash
  curl -X GET http://localhost:8000/quizzes/
  ```

## Models

### User
- `id`: UUID
- `username`: string
- `password`: string
- `role`: string (values: "teacher", "student")

### Quiz
- `id`: UUID
- `title`: string
- `teacher_id`: UUID
- `created_at`: datetime
- `questions`: list (JSON format)

### QuizSubmission
- `id`: UUID
- `quiz_id`: UUID
- `student_id`: UUID
- `answers`: list (JSON format)
- `submitted_at`: datetime

## Existing Sections
# asep-test-playground
Testing playground for ASEP application
