# Personal Budget Tracker
A web application for individuals to track personal expenses and manage budgets effortlessly.

## Setup
1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <project-directory>`
3. Install dependencies: `pip install -r requirements.txt`
4. Run database migrations: `alembic upgrade head`
5. Start the application: `uvicorn api.main:app --reload`

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
    "username": "string"
}
```
- **Curl Example:**
```bash
curl -X POST http://localhost:8000/signup -H "Content-Type: application/json" -d '{"username": "user1", "password": "password123"}'
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
    "message": "Login successful"
}
```
- **Curl Example:**
```bash
curl -X POST http://localhost:8000/login -H "Content-Type: application/json" -d '{"username": "user1", "password": "password123"}'
```

### Create Expense
- **Method:** POST
- **Path:** /expenses
- **Request Body:**
```json
{
    "amount": "integer",
    "category": "string",
    "date": "string",
    "user_id": "integer"
}
```
- **Response Shape:**
```json
{
    "amount": "integer",
    "category": "string",
    "date": "string",
    "user_id": "integer"
}
```
- **Curl Example:**
```bash
curl -X POST http://localhost:8000/expenses -H "Content-Type: application/json" -d '{"amount": 1000, "category": "Food", "date": "2023-10-01", "user_id": 1}'
```

### Read Expense
- **Method:** GET
- **Path:** /expenses/{expense_id}
- **Response Shape:**
```json
{
    "amount": "integer",
    "category": "string",
    "date": "string",
    "user_id": "integer"
}
```
- **Curl Example:**
```bash
curl -X GET http://localhost:8000/expenses/1
```

### Update Expense
- **Method:** PUT
- **Path:** /expenses/{expense_id}
- **Request Body:**
```json
{
    "amount": "integer",
    "category": "string",
    "date": "string"
}
```
- **Response Shape:**
```json
{
    "amount": "integer",
    "category": "string",
    "date": "string",
    "user_id": "integer"
}
```
- **Curl Example:**
```bash
curl -X PUT http://localhost:8000/expenses/1 -H "Content-Type: application/json" -d '{"amount": 1500, "category": "Groceries", "date": "2023-10-02"}'
```

### Delete Expense
- **Method:** DELETE
- **Path:** /expenses/{expense_id}
- **Response Shape:**
```json
{
    "detail": "string"
}
```
- **Curl Example:**
```bash
curl -X DELETE http://localhost:8000/expenses/1
```

### Get Expenses
- **Method:** GET
- **Path:** /expenses
- **Query Parameters:** `category`, `start_date`, `end_date`
- **Response Shape:**
```json
[
    {
        "amount": "integer",
        "category": "string",
        "date": "string",
        "user_id": "integer"
    }
]
```
- **Curl Example:**
```bash
curl -X GET "http://localhost:8000/expenses?category=Food"
```

### Dashboard
- **Method:** GET
- **Path:** /dashboard
- **Query Parameters:** `user_id`
- **Response Shape:**
```json
{
    "total_spent": "integer",
    "category_breakdown": {
        "category": "integer"
    }
}
```
- **Curl Example:**
```bash
curl -X GET "http://localhost:8000/dashboard?user_id=1"
```

### Create Budget
- **Method:** POST
- **Path:** /budgets
- **Request Body:**
```json
{
    "category": "string",
    "amount": "integer",
    "user_id": "integer"
}
```
- **Response Shape:**
```json
{
    "category": "string",
    "amount": "integer",
    "user_id": "integer"
}
```
- **Curl Example:**
```bash
curl -X POST http://localhost:8000/budgets -H "Content-Type: application/json" -d '{"category": "Food", "amount": 5000, "user_id": 1}'
```

### Get Budgets
- **Method:** GET
- **Path:** /budgets/{user_id}
- **Response Shape:**
```json
[
    {
        "category": "string",
        "amount": "integer",
        "user_id": "integer"
    }
]
```
- **Curl Example:**
```bash
curl -X GET http://localhost:8000/budgets/1
```

### Update Budget
- **Method:** PUT
- **Path:** /budgets/{budget_id}
- **Request Body:**
```json
{
    "amount": "integer"
}
```
- **Response Shape:**
```json
{
    "category": "string",
    "amount": "integer",
    "user_id": "integer"
}
```
- **Curl Example:**
```bash
curl -X PUT http://localhost:8000/budgets/1 -H "Content-Type: application/json" -d '{"amount": 6000}'
```

### Delete Budget
- **Method:** DELETE
- **Path:** /budgets/{budget_id}
- **Response Shape:**
```json
{
    "detail": "string"
}
```
- **Curl Example:**
```bash
curl -X DELETE http://localhost:8000/budgets/1
```

### Check Budget
- **Method:** GET
- **Path:** /budgets/check/{user_id}
- **Response Shape:**
```json
{
    "total_spent": "integer"
}
```
- **Curl Example:**
```bash
curl -X GET http://localhost:8000/budgets/check/1
```

### Budget Status
- **Method:** GET
- **Path:** /budgets/status/{user_id}
- **Response Shape:**
```json
{
    "budgets": [
        {
            "category": "string",
            "amount": "integer",
            "user_id": "integer"
        }
    ]
}
```
- **Curl Example:**
```bash
curl -X GET http://localhost:8000/budgets/status/1
```

## Models

### Expense
- **amount**: Integer, amount in cents
- **category**: String, category of the expense
- **date**: String, date of the expense
- **user_id**: Integer, foreign key to user

### Budget
- **category**: String, category of the budget
- **amount**: Integer, budget amount in cents
- **user_id**: Integer, foreign key to user

## Existing Sections
### Small Online Store
A simple web application for a small business to manage an online storefront, including product catalog, shopping cart, and checkout functionality.
