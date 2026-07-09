import pytest
from fastapi.testclient import TestClient
from your_module_name.routers.links import router  # Adjusted import to the correct module name

client = TestClient(router)

def test_create_link_sql_injection():
    response = client.post("/api/v1/links", json={"url": "http://example.com", "custom_slug": "custom123'; DROP TABLE links; --"})
    assert response.status_code == 409  # Conflict due to slug collision

def test_create_link_xss_attack():
    response = client.post("/api/v1/links", json={"url": "http://example.com", "custom_slug": "<script>alert('xss')</script>"})
    assert response.status_code == 201
    assert "<script>" not in response.json()["slug"]  # Ensure XSS is not reflected

def test_create_link_empty_url():
    response = client.post("/api/v1/links", json={"url": "", "custom_slug": "validslug"})
    assert response.status_code == 422  # Unprocessable Entity

def test_create_link_invalid_url_format():
    response = client.post("/api/v1/links", json={"url": "ftp://example.com", "custom_slug": "validslug"})
    assert response.status_code == 422  # Unprocessable Entity

def test_create_link_missing_url():
    response = client.post("/api/v1/links", json={"custom_slug": "validslug"})
    assert response.status_code == 422  # Unprocessable Entity

def test_create_link_custom_slug_with_special_characters():
    response = client.post("/api/v1/links", json={"url": "http://example.com", "custom_slug": "invalid_slug!"})
    assert response.status_code == 422  # Unprocessable Entity

def test_create_link_response_headers():
    response = client.post("/api/v1/links", json={"url": "http://example.com"})
    assert "X-Content-Type-Options" in response.headers
    assert response.headers["X-Content-Type-Options"] == "nosniff"

def test_create_link_sensitive_data_exposure():
    response = client.post("/api/v1/links", json={"url": "http://example.com"})
    assert "password" not in response.json()  # Ensure no sensitive data is leaked