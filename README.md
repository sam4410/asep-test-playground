# Freelancer Invoice Tracker
A React Native/Expo mobile application with a FastAPI backend for freelancers to track client invoices with paid/unpaid status, utilizing Clerk for managed authentication.

## Setup
1. **Backend Setup**
   - Ensure you have Python 3.7+ installed.
   - Create a virtual environment and activate it.
   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```
   - Set environment variables:
     ```
     export CLERK_SECRET_KEY=your_clerk_secret_key
     export ALLOWED_ORIGIN=your_allowed_origin
     export DATABASE_URL=your_database_url
     ```
   - Run the FastAPI server:
     ```
     uvicorn backend.main:app --reload
     ```

2. **Frontend Setup**
   - Ensure you have Node.js installed.
   - Navigate to the `frontend` directory.
   - Install dependencies:
     ```
     npm install
     ```
   - Build the EAS dev client:
     ```
     eas build --profile development --platform ios
     ```
   - Run the Expo app:
     ```
     npm start
     ```

## API Endpoints
### GET /
- **Response**: 
  ```json
  { "message": "Welcome to the Freelancer Invoice Tracker API" }
  ```
- **Curl Example**:
  ```
  curl http://localhost:8000/
  ```

### POST /invoices/
- **Request Body**:
  ```json
  {
    "client_name": "string",
    "amount": "integer",
    "status": "string"  // 'paid' or 'unpaid'
  }
  ```
- **Response**:
  ```json
  {
    "id": "integer",
    "user_id": "integer",
    "client_name": "string",
    "amount": "integer",
    "status": "string"
  }
  ```
- **Curl Example**:
  ```
  curl -X POST http://localhost:8000/invoices/ -H "Authorization: Bearer your_token" -H "Content-Type: application/json" -d '{"client_name": "Client A", "amount": 100, "status": "unpaid"}'
  ```

### GET /invoices/
- **Response**:
  ```json
  [
    {
      "id": "integer",
      "user_id": "integer",
      "client_name": "string",
      "amount": "integer",
      "status": "string"
    }
  ]
  ```
- **Curl Example**:
  ```
  curl -X GET http://localhost:8000/invoices/ -H "Authorization: Bearer your_token"
  ```

### GET /invoices/{invoice_id}
- **Response**:
  ```json
  {
    "id": "integer",
    "user_id": "integer",
    "client_name": "string",
    "amount": "integer",
    "status": "string"
  }
  ```
- **Curl Example**:
  ```
  curl -X GET http://localhost:8000/invoices/1 -H "Authorization: Bearer your_token"
  ```

### PUT /invoices/{invoice_id}
- **Request Body**:
  ```json
  {
    "client_name": "string",
    "amount": "integer",
    "status": "string"  // 'paid' or 'unpaid'
  }
  ```
- **Response**:
  ```json
  {
    "id": "integer",
    "user_id": "integer",
    "client_name": "string",
    "amount": "integer",
    "status": "string"
  }
  ```
- **Curl Example**:
  ```
  curl -X PUT http://localhost:8000/invoices/1 -H "Authorization: Bearer your_token" -H "Content-Type: application/json" -d '{"client_name": "Client A", "amount": 150, "status": "paid"}'
  ```

### DELETE /invoices/{invoice_id}
- **Response**:
  ```json
  {
    "id": "integer",
    "user_id": "integer",
    "client_name": "string",
    "amount": "integer",
    "status": "string"
  }
  ```
- **Curl Example**:
  ```
  curl -X DELETE http://localhost:8000/invoices/1 -H "Authorization: Bearer your_token"
  ```

## Models
### User
- **id**: integer
- **clerk_user_id**: string (unique)

### Invoice
- **id**: integer
- **user_id**: integer
- **client_name**: string
- **amount**: integer
- **status**: string ('paid' or 'unpaid')
