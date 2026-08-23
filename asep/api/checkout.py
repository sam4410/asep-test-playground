from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from asep.db.models import Product  # Adjusted import to match the correct module structure
from asep.database import get_db  # Adjusted import to match the correct module structure

router = APIRouter()

class CheckoutItem(BaseModel):
    product_id: int
    quantity: int

class CheckoutRequest(BaseModel):
    items: list[CheckoutItem]

@router.post("/api/v1/checkout")
def checkout(request: CheckoutRequest, db: Session = Depends(get_db)):
    total = 0.0
    for item in request.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")
        if product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product {product.name}")
        total += product.price * item.quantity
        product.stock_quantity -= item.quantity  # Deduct the stock

    db.commit()  # Commit the transaction to save stock changes

    return {
        "message": "Checkout successful",
        "total": total
    }

app.include_router(router)  # Ensure this line is included to register the router
