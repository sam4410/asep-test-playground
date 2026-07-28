import pytest
from models.database import User
from werkzeug.security import check_password_hash

def test_signup(client):
    """Test user signup functionality."""
    response = client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })
    assert response.status_code == 302  # Should redirect after signup
    
    with client.application.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert check_password_hash(user.password, 'testpass')

def test_signup_password_mismatch(client):
    """Test signup with password mismatch."""
    response = client.post('/signup', data={
        'username': 'testuser2',
        'password': 'testpass',
        'confirm_password': 'wrongpass'
    })
    assert response.status_code == 200  # Should not redirect
    assert b'Passwords do not match.' in response.data  # Flash message check

def test_login(client):
    """Test user login functionality."""
    client.post('/signup', data={
        'username': 'testuser3',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })
    
    response = client.post('/login', data={
        'username': 'testuser3',
        'password': 'testpass'
    })
    assert response.status_code == 302  # Should redirect after login
    assert b'Login successful!' in response.data  # Flash message check

def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post('/login', data={
        'username': 'invaliduser',
        'password': 'wrongpass'
    })
    assert response.status_code == 200  # Should not redirect
    assert b'Invalid username or password.' in response.data  # Flash message check

def test_logout(client):
    """Test user logout functionality."""
    client.post('/signup', data={
        'username': 'testuser4',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })
    client.post('/login', data={
        'username': 'testuser4',
        'password': 'testpass'
    })
    
    response = client.get('/logout')
    assert response.status_code == 302  # Should redirect after logout
    assert b'You have been logged out.' in response.data  # Flash message check
    with client.application.app_context():
        user = User.query.filter_by(username='testuser4').first()
        assert user is not None
        assert 'user_id' not in client.session  # User should be logged out

def test_logout_without_login(client):
    """Test logout without being logged in."""
    response = client.get('/logout')
    assert response.status_code == 302  # Should redirect