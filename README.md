# ASEP - Automated Payment Reminder Tool
A Python/Flask web application designed to help creative freelancers automate payment reminders for overdue invoices.

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
3. Set environment variables:
   ```
   export SECRET_KEY='your-secret-key'
   export INVOICE_DB_URL='sqlite:///app.db'
   ```
4. Run the application:
   ```
   python app.py
   ```

## API Endpoints

### Health Check
- **Method:** GET
- **Path:** /health
- **Response Shape:**
  ```json
  {
    "status": "ok"
  }
  ```
- **Curl Example:**
  ```
  curl http://localhost:5000/health
  ```

### List Projects
- **Method:** GET
- **Path:** /api/v1/projects
- **Response Shape:**
  ```json
  [
    {
      "id": 1,
      "name": "ASEP Platform",
      "status": "running"
    }
  ]
  ```
- **Curl Example:**
  ```
  curl http://localhost:5000/api/v1/projects
  ```

## Models
- Currently, there are no defined models in the application. Future models will be added as the application develops. 

## Existing README
# asep-test-playground
Testing playground for ASEP application
