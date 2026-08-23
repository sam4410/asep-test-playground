from .main import app  # Adjusted import to use relative path
@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    return TestClient(app)
