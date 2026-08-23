import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from api.db import models  # Adjusted import to use the correct path
from fastapi.testclient import TestClient
from api.main import app

