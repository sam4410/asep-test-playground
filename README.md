# Jewelry Dashboard - A Flask Web Application for Jewelry Artisans

A complete, runnable Python/Flask web application designed to help independent jewelry artisans manage custom orders, raw material stock, and customer payment statuses.

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```
   export DATABASE_URL=sqlite:///app.db
   export SECRET_KEY=your_secret_key
   ```

4. Run the application:
   ```
   python app.py
   ```

## API Endpoints

### User Authentication

- **POST /signup**
  - Request Body:
    - `username`: string
    - `password`: string
    - `confirm_password`: string
  - Response: Redirects to login page with flash message.
  - Example:
    ```
    curl -X POST http://localhost:5000/signup -d "username=testuser&password=testpass&confirm_password=testpass"
    ```

- **POST /login**
  - Request Body:
    - `username`: string
    - `password`: string
  - Response: Redirects to dashboard with flash message.
  - Example:
    ```
    curl -X POST http://localhost:5000/login -d "username=testuser&password=testpass"
    ```

- **GET /logout**
  - Response: Redirects to login page with flash message.
  - Example:
    ```
    curl http://localhost:5000/logout
    ```

### Dashboard

- **GET /dashboard**
  - Response: Renders dashboard template with active orders, materials, and overdue payments.
  - Example:
    ```
    curl http://localhost:5000/dashboard
    ```

### Orders Management

- **GET /orders**
  - Response: Renders orders management template.
  - Example:
    ```
    curl http://localhost:5000/orders
    ```

- **POST /orders**
  - Request Body:
    - `customer_name`: string
    - `status`: string
    - `total`: float
  - Response: Redirects to orders management with flash message.
  - Example:
    ```
    curl -X POST http://localhost:5000/orders -d "customer_name=Alice&status=Pending&total=150.0"
    ```

### Materials Management

- **GET /materials**
  - Response: Renders materials management template.
  - Example:
    ```
    curl http://localhost:5000/materials
    ```

- **POST /materials**
  - Request Body:
    - `name`: string
    - `stock_level`: integer
  - Response: Redirects to materials management with flash message.
  - Example:
    ```
    curl -X POST http://localhost:5000/materials -d "name=Gold&stock_level=20"
    ```

### Payments Management

- **GET /payments**
  - Response: Renders payments management template.
  - Example:
    ```
    curl http://localhost:5000/payments
    ```

## Models

### User
- `id`: Integer, primary key
- `username`: String, unique, not nullable
- `password`: String, not nullable

### Order
- `id`: Integer, primary key
- `customer_name`: String, not nullable
- `status`: String, not nullable
- `total`: Float, not nullable
- `user_id`: Integer, foreign key, not nullable

### Material
- `id`: Integer, primary key
- `name`: String, not nullable
- `stock_level`: Integer, not nullable
- `user_id`: Integer, foreign key, not nullable

### Payment
- `id`: Integer, primary key
- `order_id`: Integer, foreign key, not nullable
- `amount`: Float, not nullable
- `status`: String, not nullable
