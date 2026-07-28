import pytest
from app import create_app
from extensions import db
import sys
sys.path.insert(0, '.')  # Add the root directory to the path
@pytest.fixture
def app():
