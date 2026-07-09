import pytest
from fastapi.testclient import TestClient
from your_project_name.routers.links import router  # Replace 'your_project_name' with the actual package name

client = TestClient(router)

def test_create_link_performance(benchmark):
    # Benchmark the creation of a link with a valid URL
    result = benchmark(client.post, "/api/v1/links", json={"url": "http://example.com"})
    assert result.status_code == 201
    assert "id" in result.json()
    assert result.json()["original_url"] == "http://example.com"
    assert len(result.json()["slug"]) == 8
    assert result.json()["created_at"] is not None

def test_create_link_with_custom_slug_performance(benchmark):
    # Benchmark the creation of a link with a custom slug
    result = benchmark(client.post, "/api/v1/links", json={"url": "http://example.com", "custom_slug": "custom123"})
    assert result.status_code == 201
    assert result.json()["slug"] == "custom123"