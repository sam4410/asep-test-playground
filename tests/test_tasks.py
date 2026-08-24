from asep.api.main import app  # Corrected import statement to reflect the correct module path
import pytest
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))