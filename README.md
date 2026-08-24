# Online Store
A small online store where customers can browse products, add items to their cart, and check out.

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
