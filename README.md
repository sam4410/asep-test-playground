# Personal Budget Tracker
A simple web application to help individuals track their personal expenses and manage budgets effectively.

## Setup
1. Clone the repository:
   ```
   git clone <repository-url>
   cd personal-budget-tracker
   ```
2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python api/main.py
   ```

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
    "message": "User created successfully",
    "username": "string",
    "id": "integer"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST http://localhost:8000/signup -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass"}'
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
    "message": "Login successful",
    "username": "string",
    "id": "integer"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST http://localhost:8000/login -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass"}'
  ```

### Create Transaction
- **Method:** POST
- **Path:** /transactions
- **Request Body:**
  ```json
  {
    "amount": "integer",
    "category": "string",
    "date": "string",
    "note": "string"
  }
  ```
- **Response Shape:**
  ```json
  {
    "amount": "integer",
    "category": "string",
    "date": "string",
    "note": "string"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST http://localhost:8000/transactions -H "Content-Type: application/json" -d '{"amount": 1000, "category": "Food", "date": "2023-10-01", "note": "Grocery shopping"}'
  ```

### Update Transaction
- **Method:** PUT
- **Path:** /transactions/{transaction_id}
- **Request Body:**
  ```json
  {
    "amount": "integer",
    "category": "string",
    "date": "string",
    "note": "string"
  }
  ```
- **Response Shape:**
  ```json
  {
    "amount": "integer",
    "category": "string",
    "date": "string",
    "note": "string"
  }
  ```
- **Curl Example:**
  ```
  curl -X PUT http://localhost:8000/transactions/1 -H "Content-Type: application/json" -d '{"amount": 1500}'
  ```

### Delete Transaction
- **Method:** DELETE
- **Path:** /transactions/{transaction_id}
- **Response Shape:**
  ```json
  {
    "detail": "Transaction deleted successfully"
  }
  ```
- **Curl Example:**
  ```
  curl -X DELETE http://localhost:8000/transactions/1
  ```

### Get Transactions
- **Method:** GET
- **Path:** /transactions
- **Response Shape:**
  ```json
  [
    {
      "amount": "integer",
      "category": "string",
      "date": "string",
      "note": "string"
    }
  ]
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/transactions
  ```

### Get Transaction by ID
- **Method:** GET
- **Path:** /transactions/{transaction_id}
- **Response Shape:**
  ```json
  {
    "amount": "integer",
    "category": "string",
    "date": "string",
    "note": "string"
  }
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/transactions/1
  ```

### Dashboard Data
- **Method:** GET
- **Path:** /dashboard
- **Response Shape:**
  ```json
  {
    "total_spent": "integer",
    "category_breakdown": {
      "category": "total"
    }
  }
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/dashboard
  ```

### Create Budget
- **Method:** POST
- **Path:** /budgets/
- **Request Body:**
  ```json
  {
    "category": "string",
    "monthly_budget": "integer"
  }
  ```
- **Response Shape:**
  ```json
  {
    "category": "string",
    "monthly_budget": "integer"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST http://localhost:8000/budgets/ -H "Content-Type: application/json" -d '{"category": "Food", "monthly_budget": 5000}'
  ```

### Update Budget
- **Method:** PUT
- **Path:** /budgets/{category}
- **Request Body:**
  ```json
  {
    "monthly_budget": "integer"
  }
  ```
- **Response Shape:**
  ```json
  {
    "monthly_budget": "integer"
  }
  ```
- **Curl Example:**
  ```
  curl -X PUT http://localhost:8000/budgets/Food -H "Content-Type: application/json" -d '{"monthly_budget": 6000}'
  ```

### Get Budget by Category
- **Method:** GET
- **Path:** /budgets/{category}
- **Response Shape:**
  ```json
  {
    "category": "string",
    "monthly_budget": "integer"
  }
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/budgets/Food
  ```

### Get All Budgets
- **Method:** GET
- **Path:** /budgets/
- **Response Shape:**
  ```json
  {
    "budgets": [
      {
        "category": "string",
        "monthly_budget": "integer"
      }
    ]
  }
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/budgets/
  ```

### Filter Transactions
- **Method:** GET
- **Path:** /transactions/filter
- **Query Parameters:**
  - category: string (optional)
  - start_date: string (optional)
  - end_date: string (optional)
- **Response Shape:**
  ```json
  [
    {
      "amount": "integer",
      "category": "string",
      "date": "string",
      "note": "string"
    }
  ]
  ```
- **Curl Example:**
  ```
  curl -X GET "http://localhost:8000/transactions/filter?category=Food&start_date=2023-10-01&end_date=2023-10-31"
  ```

## Models

### User
- **Fields:**
  - id: integer
  - username: string
  - password: string (hashed)

### Transaction
- **Fields:**
  - id: integer
  - amount: integer (in cents)
  - category: string
  - date: string (ISO format)
  - note: string (optional)

### Budget
- **Fields:**
  - id: integer
  - category: string
  - monthly_budget: integer (in cents)

## Setup
1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <project-directory>`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up the database: Follow the instructions in the database setup documentation.
5. Run the application: `python asep/api/main.py` (or the appropriate command for your setup).

## API Endpoints

### Get Products
- **Method:** GET
- **Path:** /api/v1/products
- **Response Shape:**
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "description": "string",
      "price": "float",
      "stock": "integer"
    }
  ]
  ```
- **Curl Example:**
  ```bash
  curl -X GET http://localhost:8000/api/v1/products
  ```

### Add to Cart
- **Method:** POST
- **Path:** /api/v1/cart/add
- **Request Body:**
  ```json
  {
    "user_id": "integer",
    "product_id": "integer",
    "quantity": "integer"
  }
  ```
- **Response Shape:**
  ```json
  {
    "message": "string",
    "cart_item": {
      "id": "integer",
      "cart_id": "integer",
      "product_id": "integer",
      "quantity": "integer"
    }
  }
  ```
- **Curl Example:**
  ```bash
  curl -X POST http://localhost:8000/api/v1/cart/add -H "Content-Type: application/json" -d '{"user_id": 1, "product_id": 1, "quantity": 2}'
  ```

### Get Order History
- **Method:** GET
- **Path:** /api/v1/orders
- **Query Parameters:** `user_id` (integer)
- **Response Shape:**
  ```json
  [
    {
      "id": "integer",
      "user_id": "integer",
      "product_id": "integer",
      "quantity": "integer",
      "order_date": "string",
      "status": "string"
    }
  ]
  ```
- **Curl Example:**
  ```bash
  curl -X GET "http://localhost:8000/api/v1/orders?user_id=1"
  ```

### Checkout
- **Method:** POST
- **Path:** /api/v1/checkout
- **Request Body:**
  ```json
  {
    "user_id": "integer",
    "cart_items": [
      {
        "product_id": "integer",
        "quantity": "integer"
      }
    ]
  }
  ```
- **Response Shape:**
  ```json
  {
    "message": "string",
    "total_amount": "float"
  }
  ```
- **Curl Example:**
  ```bash
  curl -X POST http://localhost:8000/api/v1/checkout -H "Content-Type: application/json" -d '{"user_id": 1, "cart_items": [{"product_id": 1, "quantity": 2}]}'
  ```

## Models

### Product
- `id`: Integer
- `name`: String
- `description`: String
- `price`: Float
- `stock`: Integer

### ShoppingCart
- `id`: Integer
- `user_id`: Integer

### CartItem
- `id`: Integer
- `cart_id`: Integer
- `product_id`: Integer
- `quantity`: Integer

### OrderHistory
- `id`: Integer
- `user_id`: Integer
- `product_id`: Integer
- `quantity`: Integer
- `order_date`: String (ISO 8601 format)
- `status`: String

## Existing Sections
# asep-test-playground
Testing playground for ASEP application
