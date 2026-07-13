import pytest
import sys
from flask import Flask, session
from your_application import db
from your_application.models import User
from routes.auth import init_app

sys.modules['flask'] = __import__('flask', fromlist=['Flask', 'session'])

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

def test_signup(app):
    with app.test_client() as client:
        response = client.post('/signup', data={'username': 'testuser', 'password': 'testpass'})
        assert response.status_code == 302  # Redirect after signup
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.username == 'testuser'

def test_signup_existing_user(app):
    with app.test_client() as client:
        client.post('/signup', data={'username': 'testuser', 'password': 'testpass'})
        response = client.post('/signup', data={'username': 'testuser', 'password': 'newpass'})
        assert response.status_code == 302  # Redirect after trying to sign up existing user
        assert 'Username already exists.' in session['_flashes'][0][1]

def test_login(app):
    with app.test_client() as client:
        client.post('/signup', data={'username': 'testuser', 'password': 'testpass'})
        response = client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        assert response.status_code == 302  # Redirect after login
        assert session['user_id'] is not None

def test_login_invalid_credentials(app):
    with app.test_client() as client:
        response = client.post('/login', data={'username': 'invaliduser', 'password': 'wrongpass'})
        assert response.status_code == 200  # Stay on login page
        assert 'Invalid username or password.' in session['_flashes'][0][1]

def test_logout(app):
    with app.test_client() as client:
        client.post('/signup', data={'username': 'testuser', 'password': 'testpass'})
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        response = client.get('/logout')
        assert response.status_code == 302  # Redirect after logout
        assert 'user_id' not in session