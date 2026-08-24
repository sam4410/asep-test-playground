# Weather Lookup API
A simple weather-lookup API that provides random weather data for a specified city.

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
   python asep/api/main.py
   ```

## API Endpoints
### GET /api/v1/weather/{city}
- **Request Path Parameter:**
  - `city` (string): The name of the city to look up.

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
curl -X GET "http://localhost:8000/api/v1/weather/London"
```

## Models
### WeatherResponse
- `city` (string): Name of the city.
- `temperature` (float): Randomly generated temperature.
- `condition` (string): Weather condition (sunny, rainy, cloudy).

## Existing README
# asep-test-playground
Testing playground for ASEP application
