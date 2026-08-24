from fastapi.testclient import TestClient
from api.auth import router as auth_router  # Ensure correct import path
client = TestClient(auth_router)
# Define your test cases here
