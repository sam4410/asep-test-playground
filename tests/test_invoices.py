import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import get_db, Base
from backend.main import app
from backend.models import User, Invoice

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_invoice(client, db_session):
    user = User(clerk_user_id="test_user")
    db_session.add(user)
    db_session.commit()
    
    response = client.post("/invoices/", json={"title": "Test Invoice", "amount": 100.0, "status": "unpaid"}, headers={"Authorization": f"Bearer {user.clerk_user_id}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Invoice"

def test_read_invoices(client, db_session):
    user = User(clerk_user_id="test_user")
    db_session.add(user)
    db_session.commit()
    
    response = client.get("/invoices/", headers={"Authorization": f"Bearer {user.clerk_user_id}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_invoice(client, db_session):
    user = User(clerk_user_id="test_user")
    db_session.add(user)
    db_session.commit()
    
    invoice = Invoice(title="Test Invoice", amount=100.0, status="unpaid", user_id=user.id)
    db_session.add(invoice)
    db_session.commit()
    
    response = client.get(f"/invoices/{invoice.id}", headers={"Authorization": f"Bearer {user.clerk_user_id}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Invoice"

def test_update_invoice(client, db_session):
    user = User(clerk_user_id="test_user")
    db_session.add(user)
    db_session.commit()
    
    invoice = Invoice(title="Test Invoice", amount=100.0, status="unpaid", user_id=user.id)
    db_session.add(invoice)
    db_session.commit()
    
    response = client.put(f"/invoices/{invoice.id}", json={"title": "Updated Invoice", "amount": 150.0, "status": "paid"}, headers={"Authorization": f"Bearer {user.clerk_user_id}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Invoice"

def test_delete_invoice(client, db_session):
    user = User(clerk_user_id="test_user")
    db_session.add(user)
    db_session.commit()
    
    invoice = Invoice(title="Test Invoice", amount=100.0, status="unpaid", user_id=user.id)
    db_session.add(invoice)
    db_session.commit()
    
    response = client.delete(f"/invoices/{invoice.id}", headers={"Authorization": f"Bearer {user.clerk_user_id}"})
    assert response.status_code == 200
    assert response.json() == {"detail": "Invoice deleted successfully"}