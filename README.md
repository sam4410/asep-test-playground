# Coin Flip API
A simple API that simulates a coin flip, returning either "heads" or "tails".

## Setup
1. Clone the repository.
2. Navigate to the project directory.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. To run the application, execute:
   ```
   python asep/api/main.py
   ```
5. The API will be available at `http://localhost:8000`.

## API Endpoints

### GET /api/v1/flip
- **Response Shape:**
  ```json
  {
    "result": "heads" | "tails"
  }
  ```
- **Curl Example:**
  ```
  curl -X GET http://localhost:8000/api/v1/flip
  ```

## Models
- **FlipResult**
  - `result`: string (either "heads" or "tails")
