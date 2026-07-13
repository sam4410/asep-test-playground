import pytest
from flask import Flask, session
from your_application import db
from your_application.models import User, Invoice
from your_application.routes.dashboard import init_app
from datetime import datetime, timedelta

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'test_secret'
    init_app(app)
    with app.app_context():
        db.create_all()
        # Create a test user and invoice
        user = User(username='testuser', password='testpass')
        db.session.add(user)
        db.session.commit()
        invoice = Invoice(user_id=user.id, client_email='client@example.com', 
                          due_date=datetime.now() - timedelta(days=1), reminder_sent=False)
        db.session.add(invoice)
        db.session.commit()
    yield app
    with app.app_context():
        db.drop_all()

def test_dashboard_view(app):
    with app.test_client() as client:
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b'Dashboard' in response.data  # Check if 'Dashboard' is in the response
        assert b'client@example.com' in response.data  # Check if the invoice is listed

def test_dashboard_view_not_logged_in(app):
    with app.test_client() as client:
        response = client.get('/dashboard')
        assert response.status_code == 302  # Should redirect to login
        with client.session_transaction() as sess:
            assert 'You need to log in to view the dashboard.' in sess['_flashes'][0][1]

def test_dashboard_view_no_invoices(app):
    with app.test_client() as client:
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        # Remove all invoices for the user
        user = User.query.filter_by(username='testuser').first()
        Invoice.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b'No invoices found.' in response.data  # Assuming this message is shown when no invoices exist

def test_dashboard_view_with_future_invoice(app):
    with app.test_client() as client:
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        # Create a future invoice
        user = User.query.filter_by(username='testuser').first()
        future_invoice = Invoice(user_id=user.id, client_email='futureclient@example.com', 
                                 due_date=datetime.now() + timedelta(days=1), reminder_sent=False)
        db.session.add(future_invoice)
        db.session.commit()
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b'futureclient@example.com' in response.data  # Check if the future invoice is listed
        assert b'client@example.com' in response.data  # Check if the past invoice is still listed
