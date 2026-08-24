import pytest
from fastapi.testclient import TestClient
from asep.api.main import app

client = TestClient(app)

def test_get_weather_performance(benchmark):
    city = "London"
    # Benchmark the performance of the weather endpoint
    response = benchmark(client.get, f"/api/v1/weather/{city}")
    assert response.status_code == 200
    data = response.json()
    assert "city" in data
    assert "temperature" in data
    assert "condition" in data
    assert isinstance(data["temperature"], float)
    assert data["condition"] in ["sunny", "rainy", "cloudy"]
import os

static_dir = "static"
if not os.path.exists(static_dir):
    os.makedirs(static_dir)  # Ensure the static directory exists before mounting

from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")