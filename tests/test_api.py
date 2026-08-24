import sys
sys.path.insert(0, './')  # Ensure the root directory is in the path
from fastapi.testclient import TestClient
from api.tasks import app

client = TestClient(app)

