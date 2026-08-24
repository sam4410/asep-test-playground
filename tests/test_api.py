import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from asep.api.dashboard import include_router  # Ensure correct import path
from fastapi.testclient import TestClient
from asep.api.main import app

