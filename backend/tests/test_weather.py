import os
import pytest

from backend.src.routes.api.v1.weather import (
    _fetch_weather,
    get_weather,
    HTTPException,
)
def test_get_weather_happy_path(monkeypatch):
    # Call the endpoint function directly
    result = get_weather(city=dummy_city)
    assert result == expected_result
def test_get_weather_missing_city_parameter():
    # Calling the endpoint without the required parameter should raise a TypeError
    with pytest.raises(TypeError):
        get_weather()  # missing required positional argument 'city'