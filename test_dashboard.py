import json
from app import create_app
import pytest

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_dashboard_access(client):
    # First, sign up and log in the user
    client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })

    # Now, access the dashboard
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Dashboard' in response.data  # Assuming 'Dashboard' is in the dashboard template

def test_dashboard_no_auth(client):
    # Try to access the dashboard without logging in
    response = client.get('/dashboard')
    assert response.status_code == 302  # Should redirect to login
    assert b'Login' in response.data  # Assuming 'Login' is in the login template

def test_dashboard_data_display(client):
    # First, sign up and log in the user
    client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })

    # Add some data to the dashboard (this would be your core feature)
    # Assuming there's an endpoint to create a new order or material
    client.post('/feature/create', data={
        'name': 'New Order',
        'status': 'Pending'
    })

    # Now, access the dashboard
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'New Order' in response.data  # Check if the new order is displayed