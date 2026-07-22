# asep-test-playground
Testing playground for ASEP application with redesigned Flask HTML templates using Tailwind CSS.

## Setup
1. Clone the repository:
   ```
   git clone <repository-url>
   cd asep-test-playground
   ```
2. Build and run the Docker container:
   ```
   docker build -t my-flask-app .
   docker run -p 5000:5000 my-flask-app
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## API Endpoints
### Login
- **Method:** POST
- **Path:** /login
- **Request Body:**
  - `username`: string (required)
  - `password`: string (required)
- **Response Shape:**
  - Redirects to dashboard on success.
  - Flash message on failure.
- **Curl Example:**
  ```
  curl -X POST http://localhost:5000/login -d "username=testuser&password=password"
  ```

### Signup
- **Method:** POST
- **Path:** /signup
- **Request Body:**
  - `username`: string (required)
  - `email`: string (required)
  - `password`: string (required)
- **Response Shape:**
  - Redirects to dashboard on success.
  - Flash message on failure.
- **Curl Example:**
  ```
  curl -X POST http://localhost:5000/signup -d "username=newuser&email=newuser@example.com&password=password"
  ```

### Dashboard
- **Method:** GET
- **Path:** /dashboard
- **Response Shape:**
  - Renders dashboard.html with user statistics and recent orders.
- **Curl Example:**
  ```
  curl http://localhost:5000/dashboard
  ```

### Feature
- **Method:** GET
- **Path:** /feature
- **Response Shape:**
  - Renders feature.html with detailed information about application features.
- **Curl Example:**
  ```
  curl http://localhost:5000/feature
  ```

## Models
- **User**
  - `username`: string
  - `email`: string
  - `password`: string

## Existing Sections
- Testing is facilitated through unit tests located in `tests/test_templates.py` and end-to-end tests in `tests/test_e2e_user_flows.py`.
