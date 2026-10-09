def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_rejects_unsupported_method(client):
    response = client.post("/health", json={})
    assert response.status_code == 405
    assert response.json()["detail"] == "Method Not Allowed"