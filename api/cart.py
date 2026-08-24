from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import Product
from database import get_db
from pydantic import BaseModel

router = APIRouter()

class CartItem(BaseModel):
    product_id: int
    quantity: int

class Cart(BaseModel):
    items: list[CartItem]

@router.post("/cart", response_model=Cart)
def add_to_cart(cart: Cart, db: Session = Depends(get_db)):
    total_price = 0.0
    for item in cart.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product {product.name}")
        total_price += product.price * item.quantity

    return {"items": cart.items, "total_price": total_price}

@router.get("/cart/total", response_model=float)
def compute_cart_total(cart: Cart, db: Session = Depends(get_db)):
    total_price = 0.0
    for item in cart.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")
        total_price += product.price * item.quantity

    return total_price

from fastapi import FastAPI
app = FastAPI()
app.include_router(router, prefix="/api/v1")

import os
static_dir = "static"
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

from starlette.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")