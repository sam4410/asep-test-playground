import pytest
from fastapi.testclient import TestClient
from api.expenses import router
from main import app  # Ensure this import is correct based on your project structure

app.include_router(router)