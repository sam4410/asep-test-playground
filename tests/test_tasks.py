import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from asep.api.main import app  # Ensure correct import pathfrom fastapi.testclient import TestClient
from asep.api.main import app