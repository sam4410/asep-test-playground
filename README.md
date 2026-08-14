# Jewelry Artisan App
A Flask web application for independent jewelry artisans to manage custom orders, material stock, and payment statuses.

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

### Authentication
- **POST /signup**
  - Request Body: 
    - `username`: string (required)
    - `password`: string (required)
  - Response: Redirects to login page or flashes a success message.
  - Example:
    ```
    curl -X POST -d "username=testuser&password=testpass" http://localhost:5000/signup
    ```

- **POST /login**
  - Request Body: 
    - `username`: string (required)
    - `password`: string (required)
  - Response: Redirects to dashboard or flashes an error message.
  - Example:
    ```
    curl -X POST -d "username=testuser&password=testpass" http://localhost:5000/login
    ```

- **GET /logout**
  - Response: Redirects to login page with a logout message.
  - Example:
    ```
    curl http://localhost:5000/logout
    ```

### Dashboard
- **GET /dashboard**
  - Response: Renders the dashboard page with user orders and stock levels.
  - Example:
    ```
    curl http://localhost:5000/dashboard
    ```

### Orders Management
- **GET /orders**
  - Response: Renders the orders management page with a list of orders.
  - Example:
    ```
    curl http://localhost:5000/orders
    ```

- **POST /orders**
  - Request Body: 
    - `material_requirements`: string (required)
    - `stock_level`: integer (required)
    - `payment_status`: string (required, values: "paid", "overdue")
  - Response: Redirects to orders page with a success message.
  - Example:
    ```
    curl -X POST -d "material_requirements=Gold&stock_level=10&payment_status=paid" http://localhost:5000/orders
    ```

- **POST /orders/<int:order_id>/delete**
  - Response: Redirects to orders page with a success message.
  - Example:
    ```
    curl -X POST http://localhost:5000/orders/1/delete
    ```

## Models
### User
- `id`: Integer, primary key
- `username`: String, unique, not nullable
- `password`: String, not nullable

### Order
- `id`: Integer, primary key
- `user_id`: Integer, foreign key to User, not nullable
- `material_requirements`: String, not nullable
- `stock_level`: Integer, not nullable
- `payment_status`: String, not nullable

### Material
- `id`: Integer, primary key
- `name`: String, unique, not nullable
- `quantity`: Integer, not nullable
