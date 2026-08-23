# Small Online Store
A simple web application for a small business to manage an online storefront, including product catalog, shopping cart, and checkout functionality.

## Setup
1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <project-directory>`
3. Install dependencies: `pip install -r requirements.txt`
4. Run database migrations: `alembic upgrade head`
5. Start the application: `uvicorn api.main:app --reload`

## API Endpoints

### Get Products
- **Method:** GET
- **Path:** /api/v1/products
- **Request Body:** None
- **Response Shape:**
```json
[
    {
        "id": 1,
        "name": "Product Name",
        "description": "Product Description",
        "price": 10.0,
        "stock_quantity": 100,
        "category_id": 1
    }
]
```
- **Curl Example:**
```bash
curl -X GET http://localhost:8000/api/v1/products
```

### Checkout
- **Method:** POST
- **Path:** /api/v1/checkout
- **Request Body:**
```json
{
    "1": 2,
    "2": 1
}
```
- **Response Shape:**
```json
{
    "message": "Checkout successful",
    "total": 40.0
}
```
- **Curl Example:**
```bash
curl -X POST http://localhost:8000/api/v1/checkout -H "Content-Type: application/json" -d '{"1": 2, "2": 1}'
```

## Models
### Product
- **id**: Integer, primary key
- **name**: String, not nullable
- **description**: String, nullable
- **price**: Float, not nullable
- **stock_quantity**: Integer, not nullable
- **category_id**: Integer, foreign key to categories, not nullable

## Existing README
# asep-test-playground
Testing playground for ASEP application
