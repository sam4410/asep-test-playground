# Jewelry Order Management App
A Flask web application for independent jewelry artisans to track custom orders, raw materials, and payment statuses.

## Setup
1. Clone the repository.
2. Navigate to the project directory.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up the database by running the application:
   ```
   python app.py
   ```
5. Access the application at `http://localhost:5000`.

## API Endpoints

### User Authentication
- **POST /signup**
  - Request Body: 
    - `username`: string (required)
    - `password`: string (required)
  - Response: Redirects to login page with flash message.
  - Example:
    ```
    curl -X POST http://localhost:5000/signup -d "username=testuser&password=testpassword"
    ```

- **POST /login**
  - Request Body: 
    - `username`: string (required)
    - `password`: string (required)
  - Response: Redirects to dashboard with flash message.
  - Example:
    ```
    curl -X POST http://localhost:5000/login -d "username=testuser&password=testpassword"
    ```

- **GET /logout**
  - Response: Redirects to login page with flash message.
  - Example:
    ```
    curl http://localhost:5000/logout
    ```

### Dashboard
- **GET /dashboard**
  - Response: Renders dashboard page with user order statistics.
  - Example:
    ```
    curl http://localhost:5000/dashboard
    ```

### Core Feature
- **GET /feature**
  - Response: Renders feature page for creating orders.
  - Example:
    ```
    curl http://localhost:5000/feature
    ```

- **POST /feature**
  - Request Body: 
    - `description`: string (required)
    - `materials`: array of material IDs (required)
    - `quantities`: array of quantities corresponding to materials (required)
  - Response: Redirects to feature page with flash message.
  - Example:
    ```
    curl -X POST http://localhost:5000/feature -d "description=New Order&materials[]=1&materials[]=2&quantities[]=2&quantities[]=3"
    ```

## Models

### User
- `id`: Integer, primary key
- `username`: String, unique, not nullable
- `password`: String, not nullable
- `orders`: Relationship to `Order`

### Order
- `id`: Integer, primary key
- `description`: String, not nullable
- `status`: String, default 'Pending'
- `payment_status`: String, default 'Unpaid'
- `user_id`: Integer, foreign key to `User`, not nullable

### Material
- `id`: Integer, primary key
- `name`: String, not nullable
- `quantity`: Integer, not nullable
- `orders`: Relationship to `OrderMaterial`

### OrderMaterial
- `id`: Integer, primary key
- `order_id`: Integer, foreign key to `Order`, not nullable
- `material_id`: Integer, foreign key to `Material`, not nullable
- `quantity`: Integer, not nullable

### Payment
- `id`: Integer, primary key
- `amount`: Float, not nullable
- `status`: String, default 'Pending'
- `order_id`: Integer, foreign key to `Order`, not nullable
- `user_id`: Integer, foreign key to `User`, not nullable
