# Jewelry Dashboard - A Flask Web Application for Jewelry Artisans

A complete, runnable Python/Flask web application designed to help independent jewelry artisans manage custom orders, raw material stock, and customer payment status.

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set environment variables:
   ```
   export SECRET_KEY='your-secret-key'
   export DATABASE_URL='sqlite:///app.db'
   ```
5. Run the application:
   ```
   python app.py
   ```

## API Endpoints

### User Authentication

- **Sign Up**
  - **Method:** POST
  - **Path:** /signup
  - **Request Body:**
    - `username`: string
    - `email`: string
    - `password`: string
  - **Response Shape:** Redirect to login page or error message
  - **Curl Example:**
    ```
    curl -X POST http://localhost:5000/signup -d "username=testuser&email=test@example.com&password=testpass"
    ```

- **Log In**
  - **Method:** POST
  - **Path:** /login
  - **Request Body:**
    - `username`: string
    - `password`: string
  - **Response Shape:** Redirect to dashboard or error message
  - **Curl Example:**
    ```
    curl -X POST http://localhost:5000/login -d "username=testuser&password=testpass"
    ```

- **Log Out**
  - **Method:** GET
  - **Path:** /logout
  - **Response Shape:** Redirect to login page
  - **Curl Example:**
    ```
    curl -X GET http://localhost:5000/logout
    ```

### Dashboard

- **View Dashboard**
  - **Method:** GET
  - **Path:** /dashboard
  - **Response Shape:** HTML page with dashboard stats and order details
  - **Curl Example:**
    ```
    curl -X GET http://localhost:5000/dashboard
    ```

### Core Feature - Custom Orders

- **Add Order**
  - **Method:** POST
  - **Path:** /feature/add
  - **Request Body:**
    - `customer_name`: string
    - `order_details`: string
  - **Response Shape:** Redirect to feature page or error message
  - **Curl Example:**
    ```
    curl -X POST http://localhost:5000/feature/add -d "customer_name=Alice&order_details=Custom Necklace"
    ```

- **View Orders**
  - **Method:** GET
  - **Path:** /feature
  - **Response Shape:** HTML page with current orders
  - **Curl Example:**
    ```
    curl -X GET http://localhost:5000/feature
    ```

## Models

### User
- `id`: integer (primary key)
- `username`: string
- `email`: string
- `password`: string (hashed)

### Order
- `id`: integer (primary key)
- `customer_name`: string
- `order_details`: string
- `status`: string (e.g., "Pending", "Shipped")

### Material
- `id`: integer (primary key)
- `name`: string
- `quantity`: integer

### Payment
- `id`: integer (primary key)
- `order_id`: integer (foreign key)
- `amount`: float
- `status`: string (e.g., "Paid", "Pending")
