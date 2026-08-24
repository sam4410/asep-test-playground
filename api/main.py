from fastapi import FastAPI, APIRouter
from sqlalchemy.orm import Session
from db.models import Product
from database import get_db

app = FastAPI()
router = APIRouter()

@router.get("/products")
def get_products(db: Session = next(get_db())):
    products = db.query(Product).all()
    return products

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, APIRouter, HTTPException
from sqlalchemy.orm import Session
from db.models import Product, ShoppingCart, CartItem
from database import get_db

app = FastAPI()
router = APIRouter()

@router.get("/products")
def get_products(db: Session = next(get_db())):
    products = db.query(Product).all()
    return products

@router.post("/cart/add")
def add_to_cart(user_id: int, product_id: int, quantity: int, db: Session = next(get_db())):
    # Check if the product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if the shopping cart exists for the user
    cart = db.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).first()
    if not cart:
        cart = ShoppingCart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Add the item to the cart
    cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return {"message": "Item added to cart", "cart_item": cart_item}

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)