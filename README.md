# Personal Budget Tracker
A personal budget tracker to log expenses and view spending by category.

## Setup
1. Clone the repository.
2. Navigate to the project directory.
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## API Endpoints

### Create Expense
- **Method:** POST
- **Path:** /expenses
- **Request Body:**
  ```json
  {
    "amount": float,
    "category": "string",
    "date": "YYYY-MM-DD",
    "user_id": integer
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": integer,
    "amount": float,
    "category": "string",
    "date": "YYYY-MM-DD",
    "user_id": integer
  }
  ```
- **Curl Example:**
  ```bash
  curl -X POST http://localhost:5000/expenses -H "Content-Type: application/json" -d '{"amount": 50.0, "category": "Food", "date": "2023-10-01", "user_id": 1}'
  ```

### Create Category
- **Method:** POST
- **Path:** /categories
- **Request Body:**
  ```json
  {
    "name": "string",
    "user_id": integer
  }
  ```
- **Response Shape:**
  ```json
  {
    "id": integer,
    "name": "string",
    "user_id": integer
  }
  ```
- **Curl Example:**
  ```bash
  curl -X POST http://localhost:5000/categories -H "Content-Type: application/json" -d '{"name": "Groceries", "user_id": 1}'
  ```

## Models

### Expense
- **id**: Integer, primary key
- **amount**: Float, not nullable
- **category**: String, not nullable
- **date**: Date, not nullable
- **user_id**: Integer, foreign key to users, not nullable

### Category
- **id**: Integer, primary key
- **name**: String, not nullable
- **user_id**: Integer, foreign key to users, not nullable

# asep-test-playground
Testing playground for ASEP application
