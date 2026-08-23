import pytest
from db.tasks import app  # Adjusted import to match the correct module structure
@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    return TestClient(app)
