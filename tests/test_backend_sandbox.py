import pytest
from fastapi.testclient import TestClient
from asep.api.main import app
from asep.db.models import Quote
import random

client = TestClient(app)

quotes = [
    Quote(text="The only limit to our realization of tomorrow is our doubts of today.", author="Franklin D. Roosevelt"),
    Quote(text="Life is what happens when you're busy making other plans.", author="John Lennon"),
    Quote(text="Get busy living or get busy dying.", author="Stephen King"),
    Quote(text="You have within you right now, everything you need to deal with whatever the world can throw at you.", author="Brian Tracy"),
    Quote(text="Believe you can and you're halfway there.", author="Theodore Roosevelt"),
]

def test_get_quote():
    response = client.get("/api/v1/quote")
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "author" in data
    assert isinstance(data["text"], str)
    assert isinstance(data["author"], str)
    assert len(data["text"]) > 0
    assert len(data["author"]) > 0

def test_get_quote_empty_response():
    # Simulate an empty quotes list (edge case)
    app.dependency_overrides[quotes] = lambda: []
    response = client.get("/api/v1/quote")
    assert response.status_code == 404  # Expecting a 404 for no quotes available
    assert response.json() == {"detail": "No quotes available"}

def override_static_files():
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
override_static_files()  # Ensure static files are not mounted for testing