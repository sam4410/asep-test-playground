import pytest
import sys
sys.path.insert(0, '/path/to/your/flask/app')  # Adjust this path to your Flask app

from flask import session

def test_dashboard_template(client):
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Your App' in response.data  # Check for the app title in the response
    assert b'Dashboard' in response.data  # Check for the dashboard title
    assert b'Total Orders' in response.data
    assert b'Pending Payments' in response.data
    assert b'Materials in Stock' in response.data