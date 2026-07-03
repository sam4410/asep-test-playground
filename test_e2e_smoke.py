import os
import pytest

@pytest.mark.skip(reason="E2E environment not configured in CI")
def test_placeholder_e2e():
    """
    Placeholder end‑to‑end test.
    The real E2E suite will be implemented with Playwright or Cypress.
    This test is intentionally skipped in CI to avoid missing fixtures.
    """
    base_url = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
    # Simple sanity check that the environment variable is reachable.
    assert isinstance(base_url, str) and base_url.startswith("http")
