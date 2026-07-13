import pytest
from flask import Flask, session
from your_application import db
from your_application.models import User
from routes.auth import init_app

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'test_secret'
    init_app(app)
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

def test_signup_integration(app):
    with app.test_client() as client:
        response = client.post('/signup', data={'username': 'testuser', 'password': 'testpass'})
        assert response.status_code == 302  # Redirect after signup
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.username == 'testuser'

def test_signup_existing_user_integration(app):
    with app.test_client() as client:
        client.post('/signup', data={'username': 'testuser', 'password': 'testpass'})
        response = client.post('/signup', data={'username': 'testuser', 'password': 'newpass'})
        assert response.status_code == 302  # Redirect after trying to sign up existing user
        with client.session_transaction() as sess:
            assert 'Username already exists.' in sess['_flashes'][0][1]

def test_login_integration(app):
    with app.test_client() as client:
        client.post('/signup', data={'username': 'testuser', 'password': 'testpass'})
        response = client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        assert response.status_code == 302  # Redirect after login
        assert 'user_id' in session

def test_login_invalid_credentials_integration(app):
    with app.test_client() as client:
        response = client.post('/login', data={'username': 'invaliduser', 'password': 'wrongpass'})
        assert response.status_code == 200  # Stay on login page
        with client.session_transaction() as sess:
            assert 'Invalid username or password.' in sess['_flashes'][0][1]

def test_logout_integration(app):
    with app.test_client() as client:
        client.post('/signup', data={'username': 'testuser', 'password': 'testpass'})
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        response = client.get('/logout')
        assert response.status_code == 302  # Redirect after logout
        assert 'user_id' not in session
        
def test_access_dashboard_without_login(app):
    with app.test_client() as client:
        response = client.get('/dashboard')
        assert response.status_code == 302  # Should redirect to login
        assert b'You need to log in' in response.data

def test_access_dashboard_with_login(app):
    with app.test_client() as client:
        client.post('/signup', data={'username': 'testuser', 'password': 'testpass'})
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        response = client.get('/dashboard')
        assert response.status_code == 200  # Should access dashboard
        assert b'Dashboard' in response.data  # Assuming 'Dashboard' is in the dashboard template

def test_flask_import(app):
    import flask  # Ensure Flask can be imported
    assert flask is not None