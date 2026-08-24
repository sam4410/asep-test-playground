# Online Quiz Platform
An online quiz platform where teachers can create quizzes and students can take them.

## Setup
1. Clone the repository:
   ```
   git clone <repository-url>
   cd online-quiz-platform
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

### Create Quiz
- **Method:** POST
- **Path:** /quizzes/
- **Request Body:**
  ```json
  {
    "title": "string",
    "questions": "list"
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": "UUID",
    "title": "string",
    "questions": "list",
    "teacher_id": "UUID"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST http://localhost:8000/quizzes/ -H "Content-Type: application/json" -d '{"title": "Sample Quiz", "questions": []}'
  ```

### Read Quiz
- **Method:** GET
- **Path:** /quizzes/{quiz_id}
- **Response Shape:**
  ```json
  {
    "id": "UUID",
    "title": "string",
    "questions": "list",
    "teacher_id": "UUID"
  }
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/quizzes/123e4567-e89b-12d3-a456-426614174000
  ```

### List Quizzes
- **Method:** GET
- **Path:** /quizzes/
- **Response Shape:**
  ```json
  [
    {
      "id": "UUID",
      "title": "string",
      "questions": "list",
      "teacher_id": "UUID"
    }
  ]
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/quizzes/
  ```

### Update Quiz
- **Method:** PUT
- **Path:** /quizzes/{quiz_id}
- **Request Body:**
  ```json
  {
    "title": "string",
    "questions": "list"
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": "UUID",
    "title": "string",
    "questions": "list",
    "teacher_id": "UUID"
  }
  ```
- **Curl Example:**
  ```
  curl -X PUT http://localhost:8000/quizzes/123e4567-e89b-12d3-a456-426614174000 -H "Content-Type: application/json" -d '{"title": "Updated Quiz", "questions": []}'
  ```

### Delete Quiz
- **Method:** DELETE
- **Path:** /quizzes/{quiz_id}
- **Response Shape:**
  ```json
  {
    "detail": "Quiz deleted successfully"
  }
  ```
- **Curl Example:**
  ```
  curl -X DELETE http://localhost:8000/quizzes/123e4567-e89b-12d3-a456-426614174000
  ```

### Create Question
- **Method:** POST
- **Path:** /questions/
- **Request Body:**
  ```json
  {
    "question_text": "string",
    "question_type": "string",
    "options": "list",
    "correct_answer": "string",
    "quiz_id": "UUID"
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": "integer",
    "question_text": "string",
    "question_type": "string",
    "options": "string",
    "correct_answer": "string",
    "quiz_id": "UUID"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST http://localhost:8000/questions/ -H "Content-Type: application/json" -d '{"question_text": "What is the capital of France?", "question_type": "multiple_choice", "options": ["Paris", "London", "Berlin"], "correct_answer": "Paris", "quiz_id": "123e4567-e89b-12d3-a456-426614174000"}'
  ```

### Read Question
- **Method:** GET
- **Path:** /questions/{question_id}
- **Response Shape:**
  ```json
  {
    "id": "integer",
    "question_text": "string",
    "question_type": "string",
    "options": "string",
    "correct_answer": "string",
    "quiz_id": "UUID"
  }
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/questions/1
  ```

### List Questions
- **Method:** GET
- **Path:** /questions/
- **Response Shape:**
  ```json
  [
    {
      "id": "integer",
      "question_text": "string",
      "question_type": "string",
      "options": "string",
      "correct_answer": "string",
      "quiz_id": "UUID"
    }
  ]
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/questions/
  ```

### Update Question
- **Method:** PUT
- **Path:** /questions/{question_id}
- **Request Body:**
  ```json
  {
    "question_text": "string",
    "question_type": "string",
    "options": "list",
    "correct_answer": "string"
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": "integer",
    "question_text": "string",
    "question_type": "string",
    "options": "string",
    "correct_answer": "string",
    "quiz_id": "UUID"
  }
  ```
- **Curl Example:**
  ```
  curl -X PUT http://localhost:8000/questions/1 -H "Content-Type: application/json" -d '{"question_text": "Updated Question", "question_type": "multiple_choice", "options": ["Paris", "London", "Berlin"], "correct_answer": "Paris"}'
  ```

### Delete Question
- **Method:** DELETE
- **Path:** /questions/{question_id}
- **Response Shape:**
  ```json
  {
    "detail": "Question deleted successfully"
  }
  ```
- **Curl Example:**
  ```
  curl -X DELETE http://localhost:8000/questions/1
  ```

### Submit Quiz
- **Method:** POST
- **Path:** /quizzes/submit
- **Request Body:**
  ```json
  {
    "quiz_id": "UUID",
    "student_id": "UUID",
    "answers": {
      "question_id": "string"
    }
  }
  ```
- **Response Shape:**
  ```json
  {
    "detail": "Quiz submitted successfully"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST http://localhost:8000/quizzes/submit -H "Content-Type: application/json" -d '{"quiz_id": "123e4567-e89b-12d3-a456-426614174000", "student_id": "123e4567-e89b-12d3-a456-426614174001", "answers": {"1": "Paris"}}'
  ```

### Get Quiz Results
- **Method:** GET
- **Path:** /quizzes/{quiz_id}/results
- **Response Shape:**
  ```json
  {
    "quiz_id": "UUID",
    "results": {
      "student_id": "UUID",
      "score": "integer"
    }
  }
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/quizzes/123e4567-e89b-12d3-a456-426614174000/results
  ```

## Models

### Quiz
- **Fields:**
  - id: UUID
  - title: string
  - questions: list
  - teacher_id: UUID

### Question
- **Fields:**
  - id: integer
  - question_text: string
  - question_type: string
  - options: string
  - correct_answer: string
  - quiz_id: UUID

### QuizSubmission
- **Fields:**
  - quiz_id: UUID
  - student_id: UUID
  - answers: dict

## Existing Sections
# asep-test-playground
Testing playground for ASEP application
