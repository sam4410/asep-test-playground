import pytest
import sys
sys.path.insert(0, '.')  # Add the root directory to the path
from app import create_app
@pytest.fixture(scope='session')
