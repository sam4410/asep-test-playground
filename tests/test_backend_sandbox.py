from pathlib import Path
import sys

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
