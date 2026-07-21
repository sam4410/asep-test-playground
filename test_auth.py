import pytest
from flask import session
from models.database import User
from app import create_app  # Added import for app context

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            # Create the database and tables
            db.create_all()
        yield client

def test_signup(client):
    response = client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 302  # Redirect after signup
    assert b'Sign up successful!' in response.data
    
    with client.application.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.username == 'testuser'
        assert user.password != 'testpassword'  # Password should be hashed

def test_signup_existing_user(client):
    client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = client.post('/signup', data={
        'username': 'testuser',
        'password': 'newpassword'
    })
    assert response.status_code == 302  # Redirect after failed signup
    assert b'Username already exists. Please choose a different one.' in response.data

def test_login(client):
    client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 302  # Redirect after login
    assert b'Login successful!' in response.data
    with client.application.app_context():
        assert session['username'] == 'testuser'

def test_login_invalid_credentials(client):
    response = client.post('/login', data={
        'username': 'invaliduser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 302  # Redirect after failed login
    assert b'Invalid username or password. Please try again.' in response.data

def test_logout(client):
    client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = client.get('/logout')
    assert response.status_code == 302  # Redirect after logout
    assert b'You have been logged out.' in response.data
    with client.application.app_context():
        assert 'username' not in session