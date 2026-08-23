from .main import app  # Adjusted import to use relative path
def test_create_expense(db_session):
    response = client.post("/expenses", json={
        "amount": 1000,
        "category": "Food",
        "date": "2023-10-01",
        "user_id": 1
    })
    assert response.status_code == 200
    assert response.json()["amount"] == 1000
    assert response.json()["category"] == "Food"

def test_read_expense(db_session):
    # Assuming an expense with ID 1 exists
    response = client.get("/expenses/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_expense(db_session):
    # Assuming an expense with ID 1 exists
    response = client.put("/expenses/1", json={
        "amount": 1500,
        "category": "Groceries",
        "date": "2023-10-02"
    })
    assert response.status_code == 200
    assert response.json()["amount"] == 1500
    assert response.json()["category"] == "Groceries"

def test_delete_expense(db_session):
    # Assuming an expense with ID 1 exists
    response = client.delete("/expenses/1")
    assert response.status_code == 200
    assert response.json()["detail"] == "Expense deleted successfully"

def test_get_expenses_by_category(db_session):
    response = client.get("/expenses?category=Food")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_expenses_no_results(db_session):
    response = client.get("/expenses?category=NonExistentCategory")
    assert response.status_code == 404
    assert response.json()["detail"] == "No expenses found for this category"

def test_get_expense_not_found(db_session):
    response = client.get("/expenses/999")  # Assuming this ID does not exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"

def test_update_expense_not_found(db_session):
    response = client.put("/expenses/999", json={
        "amount": 1500,
        "category": "Groceries",
        "date": "2023-10-02"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"

def test_delete_expense_not_found(db_session):
    response = client.delete("/expenses/999")  # Assuming this ID does not exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"