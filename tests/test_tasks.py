import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from fastapi.testclient import TestClient
from src.api.main import app
client = TestClient(app)

 # Add your test cases here