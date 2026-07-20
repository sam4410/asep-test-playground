import json
from app import create_app
import pytest

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_order(client):
    # First, sign up and log in the user
    client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })

    # Create a new order
    response = client.post('/feature/create', data={
        'name': 'Custom Necklace',
        'status': 'Pending'
    })
    assert response.status_code == 200
    assert b'Order created successfully' in response.data

def test_list_orders(client):
    # First, sign up and log in the user
    client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })

    # Create a new order
    client.post('/feature/create', data={
        'name': 'Custom Necklace',
        'status': 'Pending'
    })

    # List orders
    response = client.get('/feature/orders')
    assert response.status_code == 200
    assert b'Custom Necklace' in response.data

def test_update_order(client):
    # First, sign up and log in the user
    client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })

    # Create a new order
    response = client.post('/feature/create', data={
        'name': 'Custom Necklace',
        'status': 'Pending'
    })

    # Update the order
    order_id = json.loads(response.data)['id']
    response = client.post(f'/feature/update/{order_id}', data={
        'status': 'Completed'
    })
    assert response.status_code == 200
    assert b'Order updated successfully' in response.data

def test_delete_order(client):
    # First, sign up and log in the user
    client.post('/signup', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })

    # Create a new order
    response = client.post('/feature/create', data={
        'name': 'Custom Necklace',
        'status': 'Pending'
    })

    # Delete the order
    order_id = json.loads(response.data)['id']
    response = client.post(f'/feature/delete/{order_id}')
    assert response.status_code == 200
    assert b'Order deleted successfully' in response.data