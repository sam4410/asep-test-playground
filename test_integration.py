import pytest
from models.database import User, Order, Material, Payment
from werkzeug.security import check_password_hash
from extensions import db  # Added import for db

def test_dashboard_requires_auth(client):
    """Test that the dashboard requires authentication."""
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'login' in response.data.lower()  # Check for login prompt

def test_dashboard_authenticated(client):
    """Test that the dashboard loads correctly for authenticated users."""
    # First, create a user and log in
    client.post('/signup', data={
        'username': 'testuser_dashboard',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })
    client.post('/login', data={
        'username': 'testuser_dashboard',
        'password': 'testpass'
    })

    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Dashboard' in response.data  # Check for dashboard title

def test_manage_orders(client):
    """Test managing orders functionality."""
    # First, create a user and log in
    client.post('/signup', data={
        'username': 'testuser_orders',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })
    client.post('/login', data={
        'username': 'testuser_orders',
        'password': 'testpass'
    })

    # Create a new order
    response = client.post('/orders', data={
        'customer_name': 'Alice',
        'status': 'Pending',
        'total': 150.0
    })
    assert response.status_code == 302  # Should redirect after creating order

    # Check if the order was created
    with client.application.app_context():
        order = Order.query.filter_by(customer_name='Alice').first()
        assert order is not None
        assert order.status == 'Pending'

def test_manage_materials(client):
    """Test managing materials functionality."""
    # First, create a user and log in
    client.post('/signup', data={
        'username': 'testuser_materials',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })
    client.post('/login', data={
        'username': 'testuser_materials',
        'password': 'testpass'
    })

    # Create a new material
    response = client.post('/materials', data={
        'name': 'Gold',
        'stock_level': 10
    })
    assert response.status_code == 302  # Should redirect after creating material

    # Check if the material was created
    with client.application.app_context():
        material = Material.query.filter_by(name='Gold').first()
        assert material is not None
        assert material.stock_level == 10

def test_view_payments(client):
    """Test viewing payments functionality."""
    # First, create a user and log in
    client.post('/signup', data={
        'username': 'testuser_payments',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })
    client.post('/login', data={
        'username': 'testuser_payments',
        'password': 'testpass'
    })

    # Create an order and a payment
    with client.application.app_context():
        user = User.query.filter_by(username='testuser_payments').first()
        order = Order(customer_name='Bob', status='Completed', total=200.0, user_id=user.id)
        db.session.add(order)
        db.session.commit()
        
        payment = Payment(order_id=order.id, amount=200.0, status='paid')
        db.session.add(payment)
        db.session.commit()

    response = client.get('/payments')
    assert response.status_code == 200
    assert b'payments' in response.data.lower()  # Check for payments section