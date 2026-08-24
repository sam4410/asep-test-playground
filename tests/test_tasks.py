import sys
import pytest
from api.main import app  # Ensure correct import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))