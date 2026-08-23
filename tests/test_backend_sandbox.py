from db.models import Product, Habit  # Adjusted import to match the correct module structure
import pytest

@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    return TestClient(app)
