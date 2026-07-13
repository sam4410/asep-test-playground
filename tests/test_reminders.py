import pytest
import sys
from flask import Flask, session
from your_application import db
from your_application.models import User, Invoice
from routes.reminders import init_app
from datetime import datetime, timedelta

sys.modules['flask'] = __import__('flask', fromlist=['Flask', 'session'])

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

def test_reminders_view(app):
    with app.test_client() as client:
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        response = client.get('/reminders')
        assert response.status_code == 200
        assert b'client@example.com' in response.data  # Check if the invoice is listed

def test_reminders_view_not_logged_in(app):
    with app.test_client() as client:
        response = client.get('/reminders')
        assert response.status_code == 302  # Should redirect to login
        with client.session_transaction() as sess:
            assert 'You need to log in to view reminders.' in sess['_flashes'][0][1]

def test_send_reminder(app):
    with app.test_client() as client:
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        invoice = Invoice.query.first()
        response = client.post(f'/send_reminder/{invoice.id}')
        assert response.status_code == 302  # Should redirect after sending reminder
        assert invoice.reminder_sent is True  # Check if reminder_sent is updated
        with client.session_transaction() as sess:
            assert 'Payment reminder sent successfully!' in sess['_flashes'][0][1]

def test_send_reminder_not_logged_in(app):
    with app.test_client() as client:
        invoice = Invoice.query.first()
        response = client.post(f'/send_reminder/{invoice.id}')
        assert response.status_code == 302  # Should redirect to login
        with client.session_transaction() as sess:
            assert 'You need to log in to send reminders.' in sess['_flashes'][0][1]

def test_send_reminder_invalid_invoice(app):
    with app.test_client() as client:
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        response = client.post('/send_reminder/999')  # Non-existent invoice ID
        assert response.status_code == 302  # Should redirect
        with client.session_transaction() as sess:
            assert 'Invoice not found or you do not have permission to send reminders.' in sess['_flashes'][0][1]