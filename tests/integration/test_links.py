import pytest
from fastapi.testclient import TestClient
from app.api.routers.links import router
from datetime import datetime
import psycopg2
from unittest.mock import patch, MagicMock

client = TestClient(router)

@patch('app.api.routers.links.psycopg2.connect')
def test_create_link_integration(mock_connect):
    mock_cursor = MagicMock()
    mock_connect.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]
    
    response = client.post("/api/v1/links", json={"url": "http://example.com"})
    assert response.status_code == 201
    assert response.json()["original_url"] == "http://example.com"
    assert len(response.json()["slug"]) == 8
    assert response.json()["created_at"] is not None

@patch('app.api.routers.links.psycopg2.connect')
def test_create_link_with_custom_slug_integration(mock_connect):
    mock_cursor = MagicMock()
    mock_connect.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]

    response = client.post("/api/v1/links", json={"url": "http://example.com", "custom_slug": "custom123"})
    assert response.status_code == 201
    assert response.json()["slug"] == "custom123"

@patch('app.api.routers.links.psycopg2.connect')
def test_create_link_slug_conflict_integration(mock_connect):
    mock_cursor = MagicMock()
    mock_connect.return_value.cursor.return_value = mock_cursor
    mock_cursor.side_effect = [None, MagicMock(integrity_error=True)]

    response = client.post("/api/v1/links", json={"url": "http://example.com", "custom_slug": "custom123"})
    assert response.status_code == 409  # Conflict

@patch('app.api.routers.links.psycopg2.connect')
def test_create_link_invalid_url_integration(mock_connect):
    response = client.post("/api/v1/links", json={"url": "invalid-url"})
    assert response.status_code == 422  # Unprocessable Entity

@patch('app.api.routers.links.psycopg2.connect')
def test_create_link_custom_slug_too_short_integration(mock_connect):
    response = client.post("/api/v1/links", json={"url": "http://example.com", "custom_slug": "ab"})
    assert response.status_code == 422  # Unprocessable Entity

@patch('app.api.routers.links.psycopg2.connect')
def test_create_link_custom_slug_too_long_integration(mock_connect):
    response = client.post("/api/v1/links", json={"url": "http://example.com", "custom_slug": "a" * 33})
    assert response.status_code == 422  # Unprocessable Entity