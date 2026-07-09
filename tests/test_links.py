import pytest
from fastapi.testclient import TestClient
from app.routers.links import router, generate_random_slug, insert_link
from pydantic import ValidationError
from unittest.mock import patch, MagicMock
from datetime import datetime

client = TestClient(router)

def test_create_link_valid():
    response = client.post("/api/v1/links", json={"url": "http://example.com"})
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["original_url"] == "http://example.com"
    assert len(response.json()["slug"]) == 8
    assert response.json()["created_at"] is not None

def test_create_link_with_custom_slug():
    response = client.post("/api/v1/links", json={"url": "http://example.com", "custom_slug": "custom123"})
    assert response.status_code == 201
    assert response.json()["slug"] == "custom123"

def test_create_link_invalid_url():
    response = client.post("/api/v1/links", json={"url": "invalid-url"})
    assert response.status_code == 422  # Unprocessable Entity

def test_create_link_custom_slug_too_short():
    response = client.post("/api/v1/links", json={"url": "http://example.com", "custom_slug": "ab"})
    assert response.status_code == 422  # Unprocessable Entity

def test_create_link_custom_slug_too_long():
    response = client.post("/api/v1/links", json={"url": "http://example.com", "custom_slug": "a" * 33})
    assert response.status_code == 422  # Unprocessable Entity

def test_generate_random_slug():
    slug = generate_random_slug()
    assert len(slug) == 8
    assert slug.isalnum()

@patch('app.routers.links.psycopg2.connect')
def test_insert_link_success(mock_connect):
    mock_cursor = MagicMock()
    mock_connect.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]
    
    link_id = insert_link("http://example.com", "custom123")
    assert link_id == 1
    mock_cursor.execute.assert_called_once()

@patch('app.routers.links.psycopg2.connect')
def test_insert_link_slug_conflict(mock_connect):
    mock_cursor = MagicMock()
    mock_connect.return_value.cursor.return_value = mock_cursor
    mock_cursor.side_effect = [None, MagicMock(integrity_error=True)]

    with pytest.raises(Exception) as excinfo:
        insert_link("http://example.com", "custom123")
    assert excinfo.value.status_code == 409  # Conflict