# ASEP Test Playground
Testing playground for ASEP application with redesigned Flask HTML templates using Tailwind CSS.

## Setup
1. Clone the repository.
2. Navigate to the project directory.
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## API Endpoints

### Login
- **Method:** POST
- **Path:** /login
- **Request Body:**
  - `username` (string, required)
  - `password` (string, required)
- **Response Shape:** Redirects to dashboard on success or returns an error message.
- **Curl Example:**
  ```
  curl -X POST -d "username=user&password=pass" http://localhost:5000/login
  ```

### Sign Up
- **Method:** POST
- **Path:** /signup
- **Request Body:**
  - `username` (string, required)
  - `email` (string, required)
  - `password` (string, required)
- **Response Shape:** Redirects to dashboard on success or returns an error message.
- **Curl Example:**
  ```
  curl -X POST -d "username=user&email=user@example.com&password=pass" http://localhost:5000/signup
  ```

### Dashboard
- **Method:** GET
- **Path:** /dashboard
- **Response Shape:** Renders the dashboard page with an overview and recent orders.
- **Curl Example:**
  ```
  curl http://localhost:5000/dashboard
  ```

### New Order
- **Method:** GET
- **Path:** /new-order
- **Response Shape:** Renders the new order page.
- **Curl Example:**
  ```
  curl http://localhost:5000/new-order
  ```

### Logout
- **Method:** GET
- **Path:** /logout
- **Response Shape:** Redirects to the login page.
- **Curl Example:**
  ```
  curl http://localhost:5000/logout
  ```

## Models
No specific data models/schemas are defined in the current implementation. 

## Existing README
Testing playground for ASEP application.
