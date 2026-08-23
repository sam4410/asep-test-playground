from ..api.main import app  # Adjusted import to use relative path
from fastapi.testclient import TestClient
from api.db.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

def test_create_habit():
    response = client.post("/habits", json={"name": "Test Habit", "target_frequency": 1})
    assert response.status_code == 200
    assert "id" in response.json()
def test_log_habit():
    response = client.post("/habits/log", json={"habit_name": "Test Habit", "user_id": 1})
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["name"] == "Test Habit"
def test_get_habit_streak():
    response = client.post("/habits/log", json={"habit_name": "Test Habit", "user_id": 1})
    habit_id = response.json()["id"]
    
    response = client.get(f"/habits/streak/{habit_id}")
    assert response.status_code == 200
    assert "streak_count" in response.json()
    assert response.json()["streak_count"] == 0  # Default streak count should be 0
def test_get_habit_streak_not_found():
    response = client.get("/habits/streak/999")  # Assuming habit_id 999 does not exist
    assert response.status_code == 404  # Not Found for non-existent habit
    assert response.json() == {"detail": "Habit not found"}
def test_log_habit_invalid_user():
    response = client.post("/habits/log", json={"habit_name": "Test Habit", "user_id": -1})
    assert response.status_code == 422  # Unprocessable Entity for invalid input
def test_get_habits():
    response = client.get("/habits?user_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Should return a list of habits
def test_get_habits_no_habits():
    response = client.get("/habits?user_id=999")  # Assuming user_id 999 has no habits
    assert response.status_code == 200
    assert response.json() == []  # Should return an empty list
sys.path.append(str(Path(__file__).resolve().parent.parent))


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # Ensure correct path
from api.main import app  # Adjusted import to use the correct path
from fastapi.testclient import TestClient
client = TestClient(app)
def test_example():
    assert True
class MockProductRepository:
    def __init__(self, products):
        self.products = {product.id: product for product in products}

    def get_product_by_id(self, product_id):
        return self.products.get(product_id)

def test_product_creation():
    product = Product(id=1, name="Test Product", description="A product for testing", price=10.0, stock_quantity=100, category_id=1)
    assert product.id == 1
    assert product.name == "Test Product"
    assert product.price == 10.0
    assert product.stock_quantity == 100

def test_shopping_cart_add_item():
    cart = ShoppingCart()
    cart.add_item(1, 2)
    assert cart.get_cart_items() == {1: 2}

def test_shopping_cart_add_item_zero_quantity():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="Quantity must be greater than zero."):
        cart.add_item(1, 0)

def test_shopping_cart_remove_item():
    cart = ShoppingCart()
    cart.add_item(1, 2)
    cart.remove_item(1)
    assert cart.get_cart_items() == {}

def test_shopping_cart_adjust_quantity():
    cart = ShoppingCart()
    cart.add_item(1, 2)
    cart.adjust_quantity(1, 3)
    assert cart.get_cart_items() == {1: 3}

def test_shopping_cart_adjust_quantity_negative():
    cart = ShoppingCart()
    cart.add_item(1, 2)
    with pytest.raises(ValueError, match="Quantity cannot be negative."):
        cart.adjust_quantity(1, -1)

def test_shopping_cart_calculate_total():
    products = [
        Product(id=1, name="Product 1", price=10.0, stock_quantity=100, category_id=1),
        Product(id=2, name="Product 2", price=20.0, stock_quantity=100, category_id=1)
    ]
    product_repo = MockProductRepository(products)
    cart = ShoppingCart()
    cart.add_item(1, 2)  # 2 * 10.0
    cart.add_item(2, 1)  # 1 * 20.0
    total = cart.calculate_total(product_repo)
    assert total == 40.0

def test_shopping_cart_calculate_total_product_not_found():
    products = [
        Product(id=1, name="Product 1", price=10.0, stock_quantity=100, category_id=1)
    ]
    product_repo = MockProductRepository(products)
    cart = ShoppingCart()
    cart.add_item(2, 1)  # Product 2 does not exist
    total = cart.calculate_total(product_repo)
    assert total == 0.0

def test_shopping_cart_clear_cart():
    cart = ShoppingCart()
    cart.add_item(1, 2)
    cart.clear_cart()
    assert cart.get_cart_items() == {}
