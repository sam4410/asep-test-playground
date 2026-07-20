# ASEP - Autonomous Engineering Platform for Jewelry Artisans

A Flask web application designed to help independent jewelry artisans manage custom orders, raw material stock, and customer payment statuses.

## Setup
1. Clone the repository.
2. Navigate to the project directory.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```
   flask shell
   >>> from app import create_app
   >>> app = create_app()
   >>> with app.app_context():
   >>>     db.create_all()
   ```
5. Run the application:
   ```
   python app.py
   ```

## API Endpoints

### Authentication
- **POST /signup**
  - Request Body: 
    - `username`: string
    - `password`: string
  - Response: 
    - Redirects to login page with flash message.
  - Example:
    ```
    curl -X POST -d "username=testuser&password=testpass" http://localhost:5000/signup
    ```

- **POST /login**
  - Request Body: 
    - `username`: string
    - `password`: string
  - Response: 
    - Redirects to dashboard with flash message.
  - Example:
    ```
    curl -X POST -d "username=testuser&password=testpass" http://localhost:5000/login
    ```

- **GET /logout**
  - Response: 
    - Redirects to login page with flash message.
  - Example:
    ```
    curl http://localhost:5000/logout
    ```

### Dashboard
- **GET /dashboard**
  - Response: 
    - Renders dashboard template with user's orders.
  - Example:
    ```
    curl http://localhost:5000/dashboard
    ```

### Core Feature
- **POST /feature/create**
  - Request Body: 
    - `name`: string
    - `status`: string
  - Response: 
    - Redirects to dashboard with flash message.
  - Example:
    ```
    curl -X POST -d "name=Custom Necklace&status=Pending" http://localhost:5000/feature/create
    ```

- **GET /feature/orders**
  - Response: 
    - Renders feature template with user's orders.
  - Example:
    ```
    curl http://localhost:5000/feature/orders
    ```

- **POST /feature/update/<int:order_id>**
  - Request Body: 
    - `status`: string
  - Response: 
    - Redirects to dashboard with flash message.
  - Example:
    ```
    curl -X POST -d "status=Completed" http://localhost:5000/feature/update/1
    ```

- **POST /feature/delete/<int:order_id>**
  - Response: 
    - Redirects to dashboard with flash message.
  - Example:
    ```
    curl -X POST http://localhost:5000/feature/delete/1
    ```

## Models

### User
- `id`: Integer, primary key
- `username`: String, unique, not nullable
- `password`: String, not nullable

### Order
- `id`: Integer, primary key
- `name`: String, not nullable
- `status`: String, not nullable
- `user_id`: Integer, foreign key, not nullable

### Material
- `id`: Integer, primary key
- `name`: String, not nullable
- `quantity`: Integer, not nullable
- `user_id`: Integer, foreign key, not nullable
