from db.models import YourModel  # Adjusted import to use the correct path

from api.db import models  # Adjusted import to use the correct path
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from api.db.models import YourModel
from fastapi.testclient import TestClient
from api.main import app

