import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # Adjust the path to include the root directory
from src.api.expenses import router  # Corrected import statement to reflect the correct module path
from fastapi import FastAPI
from fastapi.testclient import TestClient
