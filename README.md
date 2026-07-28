# Jewelry Dashboard - A Flask Web Application for Jewelry Artisans

A complete, runnable Python/Flask web application designed to help independent jewelry artisans manage custom orders, raw material stock, and customer payment statuses.

## Setup
1. Clone the repository.
2. Navigate to the project directory.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```
   python app.py
   ```
5. Run the application:
   ```
   python app.py
   ```

## API Endpoints

### Health Check
- **Method:** GET
- **Path:** /health
- **Response:**
  ```json
  {
    "status": "ok"
  }
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:5000/health
  ```

### User Authentication
- **Sign Up**
  - **Method:** GET, POST
  - **Path:** /signup
  - **Request Body Fields:**
    - `username`: string
    - `password`: string
  - **Response:** Redirects to login on success or shows flash message on error.
  - **Curl Example:**
    ```
    curl -X POST http://localhost:5000/signup -d "username=newuser&password=newpass"
    ```

- **Log In**
  - **Method:** GET, POST
  - **Path:** /login
  - **Request Body Fields:**
    - `username`: string
    - `password`: string
  - **Response:** Redirects to dashboard on success or shows flash message on error.
  - **Curl Example:**
    ```
    curl -X POST http://localhost:5000/login -d "username=testuser&password=testpass"
    ```

- **Log Out**
  - **Method:** GET
  - **Path:** /logout
  - **Response:** Redirects to login with a flash message.
  - **Curl Example:**
    ```
    curl -X GET http://localhost:5000/logout
    ```

### Dashboard
- **View Dashboard**
  - **Method:** GET
  - **Path:** /dashboard
  - **Response:** Renders dashboard with active orders and materials.
  - **Curl Example:**
    ```
    curl -X GET http://localhost:5000/dashboard
    ```

### Orders Management
- **Manage Orders**
  - **Method:** GET, POST
  - **Path:** /orders
  - **Request Body Fields:**
    - `description`: string (for POST)
  - **Response:** Renders orders management page or redirects on order creation.
  - **Curl Example:**
    ```
    curl -X POST http://localhost:5000/orders -d "description=New Order"
    ```

- **Delete Order**
  - **Method:** POST
  - **Path:** /orders/<int:order_id>/delete
  - **Response:** Redirects to orders management page after deletion.
  - **Curl Example:**
    ```
    curl -X POST http://localhost:5000/orders/1/delete
    ```

### Dashboard Stats
- **Get Dashboard Stats**
  - **Method:** GET
  - **Path:** /dashboard/stats
  - **Response:**
  ```json
  {
    "total_orders": int,
    "total_materials": int,
    "overdue_payments": int,
    "total_revenue": float
  }
  ```
  - **Curl Example:**
  ```
  curl -X GET http://localhost:5000/dashboard/stats
  ```

## Models

### User
- `id`: Integer, primary key
- `username`: String, unique, not nullable
- `password`: String, not nullable
- `orders`: Relationship to Order

### Order
- `id`: Integer, primary key
- `description`: String, not nullable
- `status`: String, default 'pending'
- `user_id`: Integer, foreign key to User

### Material
- `id`: Integer, primary key
- `name`: String, not nullable
- `stock_level`: Integer, default 0

### Payment
- `id`: Integer, primary key
- `amount`: Float, not nullable
- `status`: String, default 'unpaid'
- `order_id`: Integer, foreign key to Order
