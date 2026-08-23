from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # Ensure correct path
from api.main import app  # Adjusted import to use the correct path
from fastapi.testclient import TestClient
client = TestClient(app)
def test_example():
    assert True
