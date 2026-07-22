import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../path/to/your/flask/app')))  # Adjust this path to your Flask app

from flask import session

def test_dashboard_template(client):
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Your App' in response.data  # Check for the app title in the response
    assert b'Dashboard' in response.data  # Check for the dashboard title
    assert b'Total Orders' in response.data
    assert b'Pending Payments' in response.data
    assert b'Materials in Stock' in response.data

def test_feature_template(client):
    # Setup: Create a user and log in
    client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })

    response = client.get('/feature')
    assert response.status_code == 200
    assert b'Feature Page' in response.data  # Check for the feature page title
    assert b'Feature Details' in response.data  # Check for feature details section

def test_signup_template(client):
    response = client.get('/signup')
    assert response.status_code == 200
    assert b'Sign Up' in response.data  # Check for the sign-up page title
    assert b'Username' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data
def test_dashboard_template(client):
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Your App' in response.data  # Check for the app title in the response
    assert b'Dashboard' in response.data  # Check for the dashboard title
    assert b'Total Orders' in response.data
    assert b'Pending Payments' in response.data
    assert b'Materials in Stock' in response.data