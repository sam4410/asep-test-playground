# Small Online Store
A simple web application for a small business to manage an online storefront, including product catalog, shopping cart, and checkout functionality.

## Setup
1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <project-directory>`
3. Install dependencies: `pip install -r requirements.txt`
4. Run database migrations: `alembic upgrade head`
5. Start the application: `uvicorn api.main:app --reload`

## API Endpoints

### Create Product
- **Method:** POST
- **Path:** /api/v1/products
- **Request Body:**
```json
{
    "name": "string",
    "description": "string",
    "price": "float",
    "stock_quantity": "integer"
}
```
- **Response Shape:**
```json
{
    "id": "integer",
    "name": "string",
    "description": "string",
    "price": "float",
    "stock_quantity": "integer"
}
```
- **Curl Example:**
```bash
curl -X POST http://localhost:8000/api/v1/products -H "Content-Type: application/json" -d '{"name": "Test Product", "description": "A product for testing", "price": 10.99, "stock_quantity": 100}'
```

### Get Product
- **Method:** GET
- **Path:** /api/v1/products/{product_id}
- **Response Shape:**
```json
{
    "id": "integer",
    "name": "string",
    "description": "string",
    "price": "float",
    "stock_quantity": "integer"
}
```
- **Curl Example:**
```bash
curl -X GET http://localhost:8000/api/v1/products/1
```

### Update Product
- **Method:** PUT
- **Path:** /api/v1/products/{product_id}
- **Request Body:**
```json
{
    "name": "string",
    "description": "string",
    "price": "float",
    "stock_quantity": "integer"
}
```
- **Response Shape:**
```json
{
    "id": "integer",
    "name": "string",
    "description": "string",
    "price": "float",
    "stock_quantity": "integer"
}
```
- **Curl Example:**
```bash
curl -X PUT http://localhost:8000/api/v1/products/1 -H "Content-Type: application/json" -d '{"name": "Updated Product", "description": "An updated product", "price": 12.99, "stock_quantity": 50}'
```

### Delete Product
- **Method:** DELETE
- **Path:** /api/v1/products/{product_id}
- **Response Shape:**
```json
{
    "detail": "string"
}
```
- **Curl Example:**
```bash
curl -X DELETE http://localhost:8000/api/v1/products/1
```

### Checkout
- **Method:** POST
- **Path:** /api/v1/checkout
- **Request Body:**
```json
{
    "items": [
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
    "total": "float"
}
```
- **Curl Example:**
```bash
curl -X POST http://localhost:8000/api/v1/checkout -H "Content-Type: application/json" -d '{"items": [{"product_id": 1, "quantity": 2}]}'
```

## Models

### Product
- **id**: Integer, primary key
- **name**: String, product name
- **description**: String, product description
- **price**: Float, product price
- **stock_quantity**: Integer, available stock quantity

## Existing Sections
### Small Online Store
A simple web application for a small business to manage an online storefront, including product catalog, shopping cart, and checkout functionality.
