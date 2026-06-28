"""
Weather endpoint implementation.

Provides a FastAPI router that exposes:
GET /api/v1/weather?city=<city_name>

The handler uses the ``requests`` library to call the OpenWeatherMap
Current Weather Data API (https://openweathermap.org/current).  An API key
must be supplied via the ``OPENWEATHER_API_KEY`` environment variable.
If the key is missing or the external request fails, a 502 Bad Gateway
response is returned.
"""

import os
from typing import Optional

import requests
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

# Base URL for the OpenWeatherMap current weather endpoint
_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def _fetch_weather(city: str) -> dict:
    """
    Internal helper that contacts the external weather service.
    Returns the parsed JSON response.
    Raises HTTPException on failure.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=502,
            detail="Weather service configuration missing (OPENWEATHER_API_KEY).",
        )

    params = {"q": city, "appid": api_key, "units": "metric"}
    try:
        resp = requests.get(_BASE_URL, params=params, timeout=5)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to retrieve weather data: {exc}",
        )

    return resp.json()


@router.get("/", summary="Get current weather for a city")
def get_weather(city: str = Query(..., description="Name of the city to query")):
    """
    Return current weather information for the specified city.
    The response mirrors the external API's JSON structure but is limited
    to a subset of fields for brevity.
    """
    data = _fetch_weather(city)

    # Extract a concise payload
    result = {
        "city": data.get("name"),
        "country": data.get("sys", {}).get("country"),
        "temperature_celsius": data.get("main", {}).get("temp"),
        "weather": data.get("weather", [{}])[0].get("description"),
        "humidity": data.get("main", {}).get("humidity"),
        "wind_speed_mps": data.get("wind", {}).get("speed"),
    }
    return result
