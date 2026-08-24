import sys
import pytest
from api.auth import router as auth_router  # Ensure correct import path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import os  # Added import for os module
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
