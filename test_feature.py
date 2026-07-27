import pytest
from flask import url_for
from extensions import db
from models.database import Order  # Assuming Order is the model for the feature

def test_add_order(client):
    # First, log in to access the feature
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'})

    response = client.post('/feature/add', data={
        'customer_name': 'Alice',
        'order_details': 'Custom Necklace'
    })
    assert response.status_code == 302  # Redirect after successful add
    with client.application.app_context():
        order = Order.query.filter_by(customer_name='Alice').first()
        assert order is not None
        assert order.order_details == 'Custom Necklace'

def test_add_order_invalid_data(client):
    # First, log in to access the feature
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'})

    response = client.post('/feature/add', data={
        'customer_name': '',  # Invalid: empty customer name
        'order_details': 'Custom Necklace'
    })
    assert response.status_code == 200  # Should return to the form with errors
    assert b'Customer Name is required' in response.data  # Assuming this is the error message

def test_view_orders(client):
    # First, log in to access the feature
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'})

    response = client.get('/feature')
    assert response.status_code == 200
    assert b'Current Orders' in response.data  # Check if the title is present

def test_view_orders_no_orders(client):
    # First, log in to access the feature
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'})

    # Clear existing orders if any
    with client.application.app_context():
        db.session.query(Order).delete()
        db.session.commit()

    response = client.get('/feature')
    assert response.status_code == 200
    assert b'No current orders' in response.data  # Assuming this is the message when no orders exist
