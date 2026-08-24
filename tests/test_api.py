import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # Adjust the path to include the root directory
from src.asep.main import app  # Corrected import statement to reflect the correct module path
import pytest

