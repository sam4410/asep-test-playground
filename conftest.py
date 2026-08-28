import os

import pytest

# Override DB URL before main.py is imported so the engine uses SQLite
os.environ.setdefault('DATABASE_URL', 'sqlite:///./test_app.db')

from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture(scope='module')
def client():
    with TestClient(app) as c:
        yield c

