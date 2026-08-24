import pytest
from fastapi.testclient import TestClient
from asep.api.main import app  # Adjusted import statement to reflect the correct module path
import os  # Added import for os module
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
