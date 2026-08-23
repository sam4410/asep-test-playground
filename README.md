# Online Quiz Platform
An online quiz platform where teachers can create quizzes and students can take them.

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

### Get Quiz
- **Method:** GET
- **Path:** /api/v1/quizzes/{quiz_id}
- **Response Shape:**
```json
{
    "id": "integer",
    "title": "string"
}
```
- **Curl Example:**
```bash
curl -X GET http://localhost:8000/api/v1/quizzes/1
```

### Update Quiz
- **Method:** PUT
- **Path:** /api/v1/quizzes/{quiz_id}
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
curl -X PUT http://localhost:8000/api/v1/quizzes/1 -H "Content-Type: application/json" -d '{"title": "Updated Quiz", "questions": []}'
```

### Delete Quiz
- **Method:** DELETE
- **Path:** /api/v1/quizzes/{quiz_id}
- **Response Shape:**
```json
{
    "detail": "string"
}
```
- **Curl Example:**
```bash
curl -X DELETE http://localhost:8000/api/v1/quizzes/1
```

### Take Quiz
- **Method:** POST
- **Path:** /api/v1/quizzes/{quiz_id}/take
- **Request Body:**
```json
[
    {
        "question_id": "integer",
        "selected_answer_id": "integer"
    }
]
```
- **Response Shape:**
```json
{
    "score": "integer"
}
```
- **Curl Example:**
```bash
curl -X POST http://localhost:8000/api/v1/quizzes/1/take -H "Content-Type: application/json" -d '[{"question_id": 1, "selected_answer_id": 1}]'
```

## Models

### Quiz
- **id**: Integer, primary key
- **title**: String, quiz title

### Question
- **id**: Integer, primary key
- **quiz_id**: Integer, foreign key to Quiz
- **text**: String, question text

### Answer
- **id**: Integer, primary key
- **question_id**: Integer, foreign key to Question
- **text**: String, answer text

### Teacher
- **id**: Integer, primary key
- **name**: String, teacher's name

## Existing Sections
### Small Online Store
A simple web application for a small business to manage an online storefront, including product catalog, shopping cart, and checkout functionality.
