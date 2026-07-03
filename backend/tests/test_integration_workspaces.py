import json
import pytest

# FastAPI is an optional dependency for these integration tests.
# If it is not installed, skip the entire module.
fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

# Import the FastAPI app defined in asep/api/main.py
from asep.api.main import app

client = TestClient(app)
