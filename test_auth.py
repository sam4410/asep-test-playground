import json
from app import create_app
import pytest

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_signup(client):
    response = client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code == 200
    assert b'Successfully signed up' in response.data

def test_login(client):
    # First, sign up the user
    client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpass'
    })

    # Now, log in
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code == 200
    assert b'Logged in successfully' in response.data

def test_logout(client):
    # First, sign up and log in the user
    client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })

    # Now, log out
    response = client.get('/logout')
    assert response.status_code == 200
    assert b'Logged out successfully' in response.data

def test_login_fail(client):
    response = client.post('/login', data={
        'username': 'wronguser',
        'password': 'wrongpass'
    })
    assert response.status_code == 401
    assert b'Invalid username or password' in response.data