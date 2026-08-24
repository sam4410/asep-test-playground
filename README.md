# Random Quote API
A simple API that returns a random quote along with its author from a predefined list.

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
   uvicorn asep.api.main:app --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### GET /api/v1/quote
- **Response Shape:**
  ```json
  {
      "text": "string",
      "author": "string"
  }
  ```
- **Curl Example:**
  ```bash
  curl -X GET http://localhost:8000/api/v1/quote
  ```

### GET /api/v1/weather/{city}
- **Path Parameters:**
  - `city`: The name of the city for which to retrieve the weather.
- **Response Shape:**
  ```json
  {
      "city": "string",
      "temperature": "float",
      "condition": "string"
  }
  ```
- **Curl Example:**
  ```bash
  curl -X GET http://localhost:8000/api/v1/weather/London
  ```

## Models

### Quote
- **Fields:**
  - `text`: `str` - The quote text.
  - `author`: `str` - The author of the quote.

### WeatherResponse
- **Fields:**
  - `city`: `str` - The name of the city.
  - `temperature`: `float` - The temperature in Celsius.
  - `condition`: `str` - The weather condition (e.g., sunny, rainy, cloudy).

## Existing README
# asep-test-playground
Testing playground for ASEP application
