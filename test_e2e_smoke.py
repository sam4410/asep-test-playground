import pytest
from app import create_app
from flask import Flask

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage_loads(client):
    """Smoke: the root URL returns a non-500 response."""
    response = client.get('/')
    assert response.status_code in (200, 302), f'Unexpected status: {response.status_code}'


def test_login_page_renders(client):
    response = client.get('/login')
    assert response.status_code in (200, 302)
    if response.status_code == 200:
        assert b'login' in response.data.lower() or b'sign' in response.data.lower()


def test_dashboard_requires_auth(client):
    response = client.get('/dashboard', follow_redirects=False)
    assert response.status_code in (302, 401, 403), \
        'Dashboard must redirect unauthenticated users'