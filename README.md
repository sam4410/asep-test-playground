# Settings Page for Account Management
This project adds a settings page for managing user account preferences such as theme and notifications.

## Setup
1. Install dependencies:
   ```
   npm install
   ```
2. Ensure you have the required Python packages for testing:
   ```
   pip install -r requirements.txt
   ```

## API Endpoints
### Fetch Settings
- **Method:** GET
- **Path:** /settings
- **Request Body:** None
- **Response Shape:**
  ```json
  {
    "theme": "string",
    "notificationsEnabled": "boolean",
    "habits": "array"
  }
  ```
- **Curl Example:**
  ```bash
  curl -X GET http://localhost:8000/settings
  ```

### Update Settings
- **Method:** POST
- **Path:** /settings
- **Request Body:**
  ```json
  {
    "theme": "string",
    "notificationsEnabled": "boolean"
  }
  ```
- **Response Shape:**
  ```json
  {
    "theme": "string",
    "notificationsEnabled": "boolean"
  }
  ```
- **Curl Example:**
  ```bash
  curl -X POST http://localhost:8000/settings -H "Content-Type: application/json" -d '{"theme": "dark", "notificationsEnabled": true}'
  ```

### Reset Settings
- **Method:** DELETE
- **Path:** /settings
- **Request Body:** None
- **Response Shape:**
  ```json
  {
    "theme": "string",
    "notificationsEnabled": "boolean"
  }
  ```
- **Curl Example:**
  ```bash
  curl -X DELETE http://localhost:8000/settings
  ```

## Models
### SettingsResponse
- **theme:** string
- **notificationsEnabled:** boolean
- **habits:** array

### SettingsUpdate
- **theme:** string
- **notificationsEnabled:** boolean

## Tests
### E2E Tests
- Located in `frontend/components/__tests__/test_e2e_settings_page.py`
