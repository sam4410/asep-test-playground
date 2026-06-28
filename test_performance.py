import time

def get_weather(city: str) -> dict:
    """
    Minimal wrapper used for performance testing.
    It imports the actual endpoint implementation lazily to avoid import side‑effects
    during test collection.
    """
    from backend.routes.weather import get_weather_for_city  # type: ignore
    return get_weather_for_city(city)


def test_weather_endpoint_performance():
    """
    Simple performance test that ensures the weather endpoint returns within a reasonable time.
    The threshold is generous to accommodate network latency in CI environments.
    """
    city = "London"
    start = time.perf_counter()
    result = get_weather(city)
    duration = time.perf_counter() - start
    # Basic sanity check on the result structure
    assert isinstance(result, dict)
    assert "temperature" in result
    # Ensure the call completes quickly (e.g., under 2 seconds)
    assert duration < 2.0, f"Weather endpoint took too long: {duration:.2f}s"
