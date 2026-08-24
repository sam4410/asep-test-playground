# Personal Budget Tracker
A personal budget tracker to log expenses and view spending by category.

## Setup
1. Clone the repository.
2. Navigate to the project directory.
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Run the database migrations:
   ```
   alembic upgrade head
   ```
5. Start the application:
   ```
   uvicorn main:app --reload
   ```

## API Endpoints

### Create Expense
- **Method:** POST
- **Path:** /expenses/
- **Request Body:**
  ```json
  {
    "amount": float,
    "category": string,
    "date": string,  // Format: YYYY-MM-DD
    "user_id": int
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": int,
    "amount": float,
    "category": string,
    "date": string,  // Format: YYYY-MM-DD
    "user_id": int
  }
  ```
- **Curl Example:**
  ```bash
  curl -X POST "http://localhost:8000/expenses/" -H "Content-Type: application/json" -d '{"amount": 50.0, "category": "Food", "date": "2023-10-01", "user_id": 1}'
  ```

### Health Check
- **Method:** GET
- **Path:** /health
- **Response Shape:**
  ```json
  {
    "status": "ok"
  }
  ```
- **Curl Example:**
  ```bash
  curl "http://localhost:8000/health"
  ```

### List Projects
- **Method:** GET
- **Path:** /api/v1/projects
- **Response Shape:**
  ```json
  [
    {
      "id": int,
      "name": string,
      "status": string
    }
  ]
  ```
- **Curl Example:**
  ```bash
  curl "http://localhost:8000/api/v1/projects"
  ```

## Models

### Expense
- **Fields:**
  - `id`: int (Primary Key)
  - `amount`: float (Not Null)
  - `category`: string (Not Null)
  - `date`: string (Not Null, Format: YYYY-MM-DD)
  - `user_id`: int (Not Null)

### Category
- **Fields:**
  - `id`: int (Primary Key)
  - `name`: string (Not Null)
  - `user_id`: int (Not Null)

## Existing README
# asep-test-playground
Testing playground for ASEP application
