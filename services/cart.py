from collections import defaultdict
from db.models import Product

class ShoppingCart:
    def __init__(self):
        self.cart = defaultdict(int)  # product_id -> quantity

    def add_item(self, product_id, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.cart[product_id] += quantity

    def remove_item(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]

    def adjust_quantity(self, product_id, quantity):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        if product_id in self.cart:
            if quantity == 0:
                self.remove_item(product_id)
            else:
                self.cart[product_id] = quantity
        else:
            raise KeyError("Product not in cart.")

    def get_cart_items(self):
        return dict(self.cart)

    def clear_cart(self):
        self.cart.clear()

    def calculate_total(self, product_repository):
        total = 0.0
        for product_id, quantity in self.cart.items():
            product = product_repository.get_product_by_id(product_id)
            if product:
                total += product.price * quantity
        return total
