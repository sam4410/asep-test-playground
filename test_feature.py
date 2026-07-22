import pytest
from flask import session
from extensions import db
from models.database import User, Order, Material, OrderMaterial

def test_feature_redirects_when_not_logged_in(client):
    response = client.get('/feature')
    assert response.status_code == 302  # Should redirect to login
    assert b'Login' in response.data

def test_feature_create_order(client):
    # Setup: Create a user and log in
    client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })

    # Setup: Create materials
    with client.application.app_context():
        material1 = Material(name='Gold', quantity=10)
        material2 = Material(name='Silver', quantity=5)
        db.session.add(material1)
        db.session.add(material2)
        db.session.commit()

    # Test: Create a new order
    response = client.post('/feature', data={
        'description': 'New Order',
        'materials': [1, 2],  # Assuming these are the IDs of the materials created
        'quantities': [2, 3]
    })
    assert response.status_code == 302  # Should redirect after creating order
    assert b'Order created successfully!' in response.data

    # Verify the order was created
    with client.application.app_context():
        order = Order.query.filter_by(description='New Order').first()
        assert order is not None
        assert order.description == 'New Order'
        assert order.user_id == session['user_id']
        assert order.status == 'Pending'

        order_materials = OrderMaterial.query.filter_by(order_id=order.id).all()
        assert len(order_materials) == 2  # Should have 2 materials linked
        assert order_materials[0].quantity == 2
        assert order_materials[1].quantity == 3

def test_feature_create_order_with_no_materials(client):
    # Setup: Create a user and log in
    client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })

    # Test: Attempt to create a new order without materials
    response = client.post('/feature', data={
        'description': 'Order with No Materials',
        'materials': [],
        'quantities': []
    })
    assert response.status_code == 302  # Should redirect
    assert b'Order created successfully!' in response.data  # Still should succeed

    # Verify the order was created
    with client.application.app_context():
        order = Order.query.filter_by(description='Order with No Materials').first()
        assert order is not None
        assert order.description == 'Order with No Materials'
        assert order.user_id == session['user_id']
        assert order.status == 'Pending'
        order_materials = OrderMaterial.query.filter_by(order_id=order.id).all()
        assert len(order_materials) == 0  # No materials should be linked