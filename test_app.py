import pytest
import sys
sys.path.insert(0, '.')  # Add the root directory to the path
from flask import Flask
from app import create_app
from extensions import db
from models.database import User  # Assuming User model is defined in models/database.py
@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

def test_signup(client):
    response = client.post('/signup', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })
    assert response.status_code == 302  # Expecting a redirect after successful signup
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user is not None

def test_login(client):
    # First, create a user
    client.post('/signup', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })

    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code == 302  # Expecting a redirect after successful login

def test_logout(client):
    # First, create and log in a user
    client.post('/signup', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })

    response = client.get('/logout')
    assert response.status_code == 302  # Expecting a redirect after logout

def test_view_dashboard(client):
    # First, create and log in a user
    client.post('/signup', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })

    response = client.get('/dashboard')
    assert response.status_code == 200  # Expecting to view the dashboard
    assert b'Dashboard' in response.data  # Check if the dashboard title is present

def test_view_orders_no_orders(client):
    # First, log in to access the feature
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'})

    response = client.get('/feature')
    assert response.status_code == 200
    assert b'No current orders' in response.data  # Assuming this is the message when no orders existimport pytest
from app import create_app
from extensions import db
import sys
sys.path.insert(0, '.')  # Add the root directory to the path

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()