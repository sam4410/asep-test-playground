# Automated Payment Reminder Tool
A Python/Flask web application for freelancers to automate payment reminders for overdue invoices.

## Setup
1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```
   export SECRET_KEY='your_secret_key'
   export DATABASE_URL='sqlite:///your_database.db'  # Optional: default is SQLite
   ```
5. Run database migrations:
   ```
   flask shell
   >>> from your_application import db
   >>> db.create_all()
   >>> exit()
   ```
6. Start the server:
   ```
   flask run
   ```

## API Endpoints

### User Authentication
- **POST /signup**
  - Request Body: 
    - `username`: string
    - `password`: string
  - Response: Redirect to login page on success or flash message on failure.
  - Example:
    ```
    curl -X POST -d "username=testuser&password=testpass" http://localhost:5000/signup
    ```

- **POST /login**
  - Request Body: 
    - `username`: string
    - `password`: string
  - Response: Redirect to dashboard on success or flash message on failure.
  - Example:
    ```
    curl -X POST -d "username=testuser&password=testpass" http://localhost:5000/login
    ```

- **GET /logout**
  - Response: Redirect to login page.
  - Example:
    ```
    curl http://localhost:5000/logout
    ```

### Dashboard
- **GET /dashboard**
  - Response: Renders the user dashboard with invoices.
  - Example:
    ```
    curl http://localhost:5000/dashboard
    ```

### Reminders
- **GET /reminders**
  - Response: Renders overdue invoices.
  - Example:
    ```
    curl http://localhost:5000/reminders
    ```

- **POST /send_reminder/<int:invoice_id>**
  - Request Body: None
  - Response: Redirect to reminders page with flash message.
  - Example:
    ```
    curl -X POST http://localhost:5000/send_reminder/1
    ```

## Models

### User
- `id`: Integer, primary key
- `username`: String, unique, not nullable
- `password`: String, not nullable

### Invoice
- `id`: Integer, primary key
- `user_id`: Integer, foreign key to User, not nullable
- `client_email`: String, not nullable
- `due_date`: DateTime, not nullable
- `reminder_sent`: Boolean, default False

## Existing README
# asep-test-playground
Testing playground for ASEP application
