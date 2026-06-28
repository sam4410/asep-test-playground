import json
import pytest

# The static payload that the Express endpoint would return.
# Duplicated here to keep the benchmark pure Python and in‑process.
CITIES_PAYLOAD = {
    "cities": [
        {"name": "New York", "country": "USA"},
        {"name": "London", "country": "UK"},
        {"name": "Tokyo", "country": "Japan"},
        {"name": "Paris", "country": "France"},
        {"name": "Sydney", "country": "Australia"},
    ]
}


def _render_cities_response():
    """
    Simulate the work performed by the Express ``/api/v1/cities`` handler:
    serialising the static ``cities`` list to JSON and returning it.
    """
    # In the real server this is ``res.json({ cities })`` – essentially
    # ``JSON.stringify`` of the payload.  ``json.dumps`` gives us a
    # comparable in‑process cost.
    return json.dumps(CITIES_PAYLOAD)


def test_cities_endpoint_performance(benchmark):
    """
    Benchmark the in‑process rendering of the cities endpoint.
    The benchmark fixture runs the callable many times and reports
    statistics.  We also assert that a single iteration stays under
    a reasonable time budget (e.g. 1 ms) to catch regressions.
    """
    # Run the benchmark – this will execute the function repeatedly.
    result = benchmark(_render_cities_response)

    # ``result`` is the return value from the last call.
    # Verify that the JSON structure is correct.
    parsed = json.loads(result)
    assert parsed == CITIES_PAYLOAD

    # Ensure the median execution time is below 1 ms (0.001 s).
    # ``benchmark.stats`` provides timing information.
    median_time = benchmark.stats.median
    assert median_time < 0.001, f"Median latency {median_time:.6f}s exceeds budget"

    # Throughput sanity check: at least 500 calls per second.
    throughput = 1.0 / median_time
    assert throughput > 500, f"Throughput {throughput:.0f} ops/s is too low"