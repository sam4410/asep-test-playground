import pytest
from fastapi.testclient import TestClient
from db.database.tasks import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
