import pytest
import sys
sys.path.insert(0, '/path/to/your/flask/app')  # Adjust the path to your Flask app
from flask import session
from extensions import db
from models.database import User, Order, Material
def test_dashboard_redirects_when_not_logged_in(client):
    response = client.get('/dashboard')
    assert response.status_code == 302  # Should redirect to login
    assert b'Login' in response.data

def test_dashboard_displays_correct_data(client):
    # Setup: Create a user and log in
    client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })

    # Setup: Create some orders and materials
    with client.application.app_context():
        user = User.query.filter_by(username='testuser').first()
        order1 = Order(description='Order 1', user_id=user.id, payment_status='Pending')
        order2 = Order(description='Order 2', user_id=user.id, payment_status='Paid')
        db.session.add(order1)
        db.session.add(order2)
        db.session.commit()

        material1 = Material(name='Gold', quantity=10)
        material2 = Material(name='Silver', quantity=5)
        db.session.add(material1)
        db.session.add(material2)
        db.session.commit()

    # Test: Access the dashboard
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Total Orders' in response.data
    assert b'Pending Payments' in response.data
    assert b'Materials in Stock' in response.data
    assert b'Order 1' in response.data
    assert b'Order 2' in response.data

def test_dashboard_no_orders_or_materials(client):
    # Setup: Create a user and log in
    client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })

    # Test: Access the dashboard with no orders or materials
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Total Orders' in response.data
    assert b'Pending Payments' in response.data
    assert b'Materials in Stock' in response.data
    assert b'Order ID' not in response.data  # No orders should be displayed