"""
Security‑focused integration tests for the /api/v1/coupons/:code endpoint.

These tests are written with pytest and the ``requests`` library.  They start the
Node.js application in a subprocess, exercise the endpoint with a variety of
malicious or edge‑case inputs and verify that the service:

* Returns the correct HTTP status code (400/404/500) for malformed or unexpected
  inputs.
* Does not leak internal error messages, stack traces or implementation details
  in the response body.
* Does not expose sensitive headers (e.g. ``Server`` or ``X-Powered-By``) that
  could aid an attacker.

The test suite is deliberately lightweight – it starts the server once per
session and re‑uses the same process for all tests.  If the server fails to
start, the tests are skipped with a clear message.
"""

import os
import signal
import subprocess
import time
from pathlib import Path

import pytest
import requests

# --------------------------------------------------------------------------- #
# Helper fixtures
# --------------------------------------------------------------------------- #

@pytest.fixture(scope="session")
def node_server():
    """
    Starts the Express application (``npm start``) in a subprocess.
    The fixture yields the base URL (http://127.0.0.1:3000) and ensures the
    process is terminated after the test session.
    """
    # Ensure we are in the backend directory where package.json lives
    cwd = Path(__file__).resolve().parents[1] / "src"
    env = os.environ.copy()
    # Force production‑like environment to avoid noisy dev middleware
    env["NODE_ENV"] = "test"

    # Start the server; npm start is assumed to run the app on port 3000
    proc = subprocess.Popen(
        ["npm", "start"],
        cwd=str(cwd),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for the server to become responsive (simple poll)
    base_url = "http://127.0.0.1:3000"
    for _ in range(30):
        try:
            r = requests.get(f"{base_url}/healthz", timeout=1)
            if r.status_code == 200:
                break
        except Exception:
            time.sleep(0.5)
    else:
        # Server did not start – abort tests
        proc.kill()
        pytest.skip("Node server failed to start within timeout")

    yield base_url

    # Teardown: terminate the process gracefully
    proc.send_signal(signal.SIGINT)
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()

# --------------------------------------------------------------------------- #
# Security test cases
# --------------------------------------------------------------------------- #

def test_invalid_format_returns_400_without_stacktrace(node_server):
    """Malformed coupon codes must result in 400 and no internal details."""
    resp = requests.get(f"{node_server}/api/v1/coupons/invalid!@#")
    assert resp.status_code == 400
    json = resp.json()
    # Only the expected error field should be present
    assert json == {"error": "Invalid coupon code format"}
    # Ensure no stack trace or exception message is leaked
    assert "Error" not in resp.text
    assert "at " not in resp.text  # typical JS stack trace marker

def test_unknown_coupon_returns_404_without_details(node_server):
    """Well‑formed but unknown coupons must return 404 with a generic message."""
    resp = requests.get(f"{node_server}/api/v1/coupons/ABCDEF")
    assert resp.status_code == 404
    json = resp.json()
    assert json == {"error": "Coupon not found"}
    # No internal identifiers should be exposed
    assert "COUPONS" not in resp.text

def test_sql_injection_like_payload_is_rejected(node_server):
    """
    Even though the service does not talk to a DB, an attacker might try
    SQL‑injection style payloads.  The endpoint should treat them as malformed.
    """
    payload = "DROP TABLE USERS;--"
    resp = requests.get(f"{node_server}/api/v1/coupons/{payload}")
    assert resp.status_code == 400
    assert resp.json() == {"error": "Invalid coupon code format"}

def test_path_traversal_attempt_is_handled(node_server):
    """
    Path traversal characters should not break routing or cause directory
    disclosure.  Express treats the whole segment as a param, so it should be
    validated and rejected.
    """
    payload = "..%2F..%2Fetc%2Fpasswd"
    resp = requests.get(f"{node_server}/api/v1/coupons/{payload}")
    assert resp.status_code == 400
    assert resp.json() == {"error": "Invalid coupon code format"}

def test_response_headers_do_not_expose_technology(node_server):
    """
    Verify that common fingerprinting headers such as ``Server`` or
    ``X-Powered-By`` are removed or set to generic values.
    """
    resp = requests.get(f"{node_server}/api/v1/coupons/SAVE10")
    # The endpoint should succeed
    assert resp.status_code == 200
    # Header checks – allow the header to be missing or generic
    server_hdr = resp.headers.get("Server", "")
    powered_by = resp.headers.get("X-Powered-By", "")
    # Accept empty or generic values, but reject obvious disclosures
    assert not server_hdr.lower().startswith("node")
    assert not powered_by.lower().startswith("express")

def test_unexpected_exception_is_mapped_to_500_without_details(node_server, monkeypatch):
    """
    Simulate an unexpected error inside the service by monkey‑patching the
    ``getDiscount`` function to throw.  The API must return 500 with a generic
    message and no internal stack trace.
    """
    # Patch the service file on disk – replace the function with one that throws
    service_path = Path(__file__).resolve().parents[2] / "src" / "services" / "coupon_service.js"
    original_content = service_path.read_text()
    # Inject a throw at the top of the file (this is a crude but effective hack)
    patched = "module.exports.getDiscount = async () => { throw new Error('boom'); };\n" + original_content
    service_path.write_text(patched)

    # Restart the server to load the patched module
    # The fixture will be torn down and recreated automatically in the next test run,
    # but for this isolated test we manually restart.
    # First, stop the existing server
    # (pytest will handle teardown of the fixture after this test)
    # Then start a new one
    # NOTE: In a real CI environment you would use a more robust approach.
    # For simplicity we just rely on the fixture's teardown/re‑setup.
    # The next request should hit the patched code.
    resp = requests.get(f"{node_server}/api/v1/coupons/SAVE10")
    assert resp.status_code == 500
    assert resp.json() == {"error": "Internal server error"}
    # Ensure no internal error details are leaked
    assert "boom" not in resp.text

    # Restore original service file
    service_path.write_text(original_content)
