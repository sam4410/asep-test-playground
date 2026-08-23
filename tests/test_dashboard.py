import pytest
from fastapi.testclient import TestClient
from db.database import tasks

@pytest.fixture(scope="module")
def client():
    with TestClient(tasks.app) as c:
        yield c
