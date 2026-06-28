import time


def test_simple_performance():
    """
    A lightweight performance test that ensures a trivial operation completes
    within a reasonable time frame. This does not rely on external fixtures
    such as ``benchmark`` from pytest-benchmark, keeping the test self‑contained.
    """
    start = time.perf_counter()
    # Perform a modest amount of work
    total = sum(range(10_000))
    duration = time.perf_counter() - start

    # Basic sanity check on the computation
    assert total == 49_995_000
    # Ensure the operation completes quickly (adjust threshold as needed)
    assert duration < 0.05, f"Operation took too long: {duration:.4f}s"