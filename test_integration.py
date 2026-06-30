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


def test_prd_deploy_check_endpoint_success(client):
    """
    Integration test that sends a GET request to the /api/v1/prd-deploy-check
    endpoint and validates the full request/response cycle.
    """
    # Perform the GET request against the endpoint
    response = client.get("/api/v1/prd-deploy-check")

    # Verify HTTP status code
    assert response.status_code == 200

    # Verify response content type is JSON
    assert response.content_type == "application/json"

    # Verify the JSON payload
    json_data = response.get_json()
    assert isinstance(json_data, dict)
    assert json_data.get("status") == "ok"

    # Ensure no unexpected keys are present
    assert set(json_data.keys()) == {"status"}