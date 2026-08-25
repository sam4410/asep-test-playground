# Freelancer Payment Reminder Dashboard
A Streamlit application for creative freelancers to manage and automate payment reminders for overdue invoices.

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
3. Run the application:
   ```
   streamlit run app.py
   ```

## API Endpoints
### Add Reminder
- **Method:** POST
- **Path:** /add_reminder
- **Request Body:**
  ```json
  {
    "client_name": "string",
    "client_relationship": "string",
    "reminder_message": "string"
  }
  ```
- **Response Shape:**
  ```json
  {
    "message": "Reminder added successfully!"
  }
  ```
- **Curl Example:**
  ```bash
  curl -X POST http://localhost:8501/add_reminder -H "Content-Type: application/json" -d '{"client_name": "Alice", "client_relationship": "Regular", "reminder_message": "Payment due next week"}'
  ```

### Load Reminders
- **Method:** GET
- **Path:** /load_reminders
- **Response Shape:**
  ```json
  [
    {
      "id": "integer",
      "client_name": "string",
      "client_relationship": "string",
      "reminder_message": "string",
      "created_at": "timestamp"
    }
  ]
  ```
- **Curl Example:**
  ```bash
  curl http://localhost:8501/load_reminders
  ```

## Models
### Reminder
- **id**: integer (Primary Key)
- **client_name**: string (Not Null)
- **client_relationship**: string (Not Null)
- **reminder_message**: string (Not Null)
- **created_at**: timestamp (Default: CURRENT_TIMESTAMP)

## Existing README
# asep-test-playground
Testing playground for ASEP application
