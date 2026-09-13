# Flask SQLite API
A minimal Python/Flask web application using SQLite for managing products.

## Setup
1. Clone the repository.
2. Navigate to the project directory.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```

## API Endpoints

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
  ```
  curl http://localhost:5000/health
  ```

### Get Products
- **Method:** GET
- **Path:** /api/products
- **Response Shape:**
  ```json
  [
    {
      "id": "string",
      "name": "string",
      "price": "float"
    }
  ]
  ```
- **Curl Example:**
  ```
  curl http://localhost:5000/api/products
  ```

### Create Product
- **Method:** POST
- **Path:** /api/products
- **Request Body Fields:**
  - `name` (string, required)
  - `price` (float, required)
- **Response Shape:**
  ```json
  {
    "id": "string",
    "name": "string",
    "price": "float"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST http://localhost:5000/api/products -H "Content-Type: application/json" -d '{"name": "Product1", "price": 10.99}'
  ```

## Models
### Product
- **id**: string (UUID, primary key)
- **name**: string (required)
- **price**: float (required, must be positive)
