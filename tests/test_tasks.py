from fastapi.testclient import TestClient
from api.main import app  # Ensure correct import path
client = TestClient(app)
# Define your test cases here