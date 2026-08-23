# Student Quiz Platform
A web application for teachers to create quizzes and assess student performance without the complexity of a full learning management system.

## Setup
1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <project-directory>`
3. Install dependencies: `pip install -r requirements.txt`
4. Run database migrations: `alembic upgrade head`
5. Start the application: `uvicorn api.main:app --reload`

## API Endpoints

### Create Quiz
- **Method:** POST
- **Path:** /api/v1/quizzes
- **Request Body:**
```json
{
    "title": "string",
    "questions": [
        {
            "text": "string",
            "correct_answer": {
                "text": "string"
            }
        }
    ]
}
```
- **Response Shape:**
```json
{
    "id": "integer",
    "title": "string"
}
```
- **Curl Example:**
```bash
curl -X POST http://localhost:8000/api/v1/quizzes -H "Content-Type: application/json" -d '{"title": "Sample Quiz", "questions": [{"text": "What is 2 + 2?", "correct_answer": {"text": "4"}}]}'
```

### Take Quiz
- **Method:** POST
- **Path:** /api/v1/quizzes/{quiz_id}/take
- **Request Body:**
```json
{
    "answers": [
        {
            "question_id": "integer",
            "selected_answer_id": "integer"
        }
    ]
}
```
- **Response Shape:**
```json
{
    "quiz_id": "integer",
    "score": "integer"
}
```
- **Curl Example:**
```bash
curl -X POST http://localhost:8000/api/v1/quizzes/1/take -H "Content-Type: application/json" -d '{"answers": [{"question_id": 1, "selected_answer_id": 1}]}'
```

### Teacher Dashboard
- **Method:** GET
- **Path:** /api/v1/teachers/{teacher_id}/dashboard
- **Response Shape:**
```json
[
    {
        "student_id": "integer",
        "quiz_id": "integer",
        "score": "integer"
    }
]
```
- **Curl Example:**
```bash
curl -X GET http://localhost:8000/api/v1/teachers/1/dashboard
```

## Models
### Quiz
- **id**: Integer, primary key
- **title**: String, not nullable
- **teacher_id**: Integer, foreign key to teachers

### Question
- **id**: Integer, primary key
- **quiz_id**: Integer, foreign key to quizzes
- **text**: String, not nullable
- **correct_answer_id**: Integer, foreign key to answers

### Answer
- **id**: Integer, primary key
- **question_id**: Integer, foreign key to questions
- **text**: String, not nullable

## Existing Sections
### Small Online Store
A simple web application for a small business to manage an online storefront, including product catalog, shopping cart, and checkout functionality.
