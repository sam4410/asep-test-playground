import pytest

# Import the Flask app instance from the application module
from app import app as flask_app
@pytest.fixture
def client():
    """
    Provide a Flask test client for making requests to the application.
    """
    # Flask provides a built‑in test client that can be used as a context manager.
    with flask_app.test_client() as client:
        yield client
