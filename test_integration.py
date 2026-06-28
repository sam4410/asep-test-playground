import re
from datetime import datetime, timezone

import pytest

# Skip the entire test module if FastAPI is not installed.
fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from asep.api.main import app

client = TestClient(app)
