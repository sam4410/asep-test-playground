import pytest
from models.database import User, Order, Material
from flask import url_for

def test_signup(client):
    response = client.post(url_for('auth.signup'), data={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code == 302  # Redirect after signup
    assert User.query.filter_by(username='testuser').first() is not None

def test_signup_existing_user(client):
    client.post(url_for('auth.signup'), data={
        'username': 'testuser',
        'password': 'testpass'
    })
    response = client.post(url_for('auth.signup'), data={
        'username': 'testuser',
        'password': 'newpass'
    })
    assert response.status_code == 302  # Redirect after signup
    assert b'Username already exists!' in response.data

def test_login(client):
    client.post(url_for('auth.signup'), data={
        'username': 'testuser',
        'password': 'testpass'
    })
    response = client.post(url_for('auth.login'), data={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code == 302  # Redirect after login
    assert b'Login successful!' in response.data

def test_login_invalid_credentials(client):
    response = client.post(url_for('auth.login'), data={
        'username': 'wronguser',
        'password': 'wrongpass'
    })
    assert response.status_code == 302  # Redirect after failed login
    assert b'Invalid username or password!' in response.data

def test_dashboard_access(client):
    client.post(url_for('auth.signup'), data={
        'username': 'testuser',
        'password': 'testpass'
    })
    client.post(url_for('auth.login'), data={
        'username': 'testuser',
        'password': 'testpass'
    })
    response = client.get(url_for('dashboard.dashboard'))
    assert response.status_code == 200

def test_orders_create(client):
    client.post(url_for('auth.signup'), data={
        'username': 'testuser',
        'password': 'testpass'
    })
    client.post(url_for('auth.login'), data={
        'username': 'testuser',
        'password': 'testpass'
    })
    response = client.post(url_for('feature.orders'), data={
        'material_requirements': 'Gold',
        'stock_level': 10,
        'payment_status': 'paid'
    })
    assert response.status_code == 302  # Redirect after creating order
    assert Order.query.count() == 1

def test_orders_create_missing_fields(client):
    client.post(url_for('auth.signup'), data={
        'username': 'testuser',
        'password': 'testpass'
    })
    client.post(url_for('auth.login'), data={
        'username': 'testuser',
        'password': 'testpass'
    })
    response = client.post(url_for('feature.orders'), data={
        'material_requirements': '',
        'stock_level': '',
        'payment_status': ''
    })
    assert response.status_code == 302  # Redirect after failed creation
    assert b'All fields are required!' in response.data

def test_delete_order(client):
    client.post(url_for('auth.signup'), data={
        'username': 'testuser',
        'password': 'testpass'
    })
    client.post(url_for('auth.login'), data={
        'username': 'testuser',
        'password': 'testpass'
    })
    order = Order(user_id=1, material_requirements='Gold', stock_level=10, payment_status='paid')
    db.session.add(order)
    db.session.commit()
    
    response = client.post(url_for('feature.delete_order', order_id=order.id))
    assert response.status_code == 302  # Redirect after deletion
    assert Order.query.count() == 0

def test_delete_order_permission(client):
    client.post(url_for('auth.signup'), data={
        'username': 'testuser',
        'password': 'testpass'
    })
    client.post(url_for('auth.login'), data={
        'username': 'testuser',
        'password': 'testpass'
    })
    order = Order(user_id=1, material_requirements='Gold', stock_level=10, payment_status='paid')
    db.session.add(order)
    db.session.commit()

    # Simulate a different user trying to delete the order
    client.post(url_for('auth.signup'), data={
        'username': 'otheruser',
        'password': 'otherpass'
    })
    client.post(url_for('auth.login'), data={
        'username': 'otheruser',
        'password': 'otherpass'
    })
    
    response = client.post(url_for('feature.delete_order', order_id=order.id))
    assert response.status_code == 302  # Redirect after failed deletion
    assert b'You do not have permission to delete this order.' in response.data