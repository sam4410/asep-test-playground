# Freelancer Invoice Tracker
A React Native/Expo mobile application with a FastAPI backend for freelancers to track client invoices and their payment status.

## Setup
1. **Backend Setup**
   - Install Python dependencies:
     ```
     pip install -r backend/requirements.txt
     ```
   - Set environment variables:
     ```
     export CLERK_SECRET_KEY=your_clerk_secret_key
     export DATABASE_URL=your_database_url
     ```
   - Run the FastAPI server:
     ```
     uvicorn backend.main:app --reload
     ```

2. **Frontend Setup**
   - Install Node.js dependencies:
     ```
     npm install
     ```
   - Ensure you have real Apple/Google developer credentials set up in the Clerk dashboard.
   - Build the EAS dev client:
     ```
     eas build --profile development
     ```
   - Run the Expo app:
     ```
     eas start
     ```

## API Endpoints
### GET /
- **Path:** `/`
- **Response:**
  ```json
  {
    "message": "Welcome to the Freelancer Invoice Tracker API"
  }
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/
  ```

### GET /invoices
- **Path:** `/invoices`
- **Response:**
  ```json
  [
    {
      "id": 1,
      "user_id": 1,
      "client_name": "Client A",
      "amount": 100,
      "status": "unpaid"
    }
  ]
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/invoices -H "Authorization: Bearer your_token"
  ```

### POST /invoices
- **Path:** `/invoices`
- **Request Body:**
  ```json
  {
    "client_name": "Client A",
    "amount": 100,
    "status": "unpaid"
  }
  ```
- **Response:**
  ```json
  {
    "id": 1,
    "user_id": 1,
    "client_name": "Client A",
    "amount": 100,
    "status": "unpaid"
  }
  ```
- **Curl Example:**
  ```
  curl -X POST http://localhost:8000/invoices -H "Authorization: Bearer your_token" -H "Content-Type: application/json" -d '{"client_name": "Client A", "amount": 100, "status": "unpaid"}'
  ```

### PUT /invoices/{invoice_id}
- **Path:** `/invoices/{invoice_id}`
- **Request Body:**
  ```json
  {
    "client_name": "Client A",
    "amount": 150,
    "status": "paid"
  }
  ```
- **Response:**
  ```json
  {
    "id": 1,
    "user_id": 1,
    "client_name": "Client A",
    "amount": 150,
    "status": "paid"
  }
  ```
- **Curl Example:**
  ```
  curl -X PUT http://localhost:8000/invoices/1 -H "Authorization: Bearer your_token" -H "Content-Type: application/json" -d '{"client_name": "Client A", "amount": 150, "status": "paid"}'
  ```

### DELETE /invoices/{invoice_id}
- **Path:** `/invoices/{invoice_id}`
- **Response:**
  ```json
  {
    "detail": "Invoice deleted successfully"
  }
  ```
- **Curl Example:**
  ```
  curl -X DELETE http://localhost:8000/invoices/1 -H "Authorization: Bearer your_token"
  ```

## Models
### User
- **id:** number
- **clerk_user_id:** string (unique)

### Invoice
- **id:** number
- **user_id:** number (foreign key to User)
- **client_name:** string
- **amount:** number
- **status:** string (values: 'paid' | 'unpaid')
