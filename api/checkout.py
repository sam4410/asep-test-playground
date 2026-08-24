from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import Product, OrderHistory
from database import get_db
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class CheckoutRequest(BaseModel):
    user_id: int
    cart_items: list[dict]  # List of dictionaries with product_id and quantity

@router.post("/checkout")
def checkout(request: CheckoutRequest, db: Session = Depends(get_db)):
    # Validate cart items and calculate total
    total_amount = 0
    for item in request.cart_items:
        product = db.query(Product).filter(Product.id == item['product_id']).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item['product_id']} not found")
        if product.stock < item['quantity']:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product ID {item['product_id']}")
        total_amount += product.price * item['quantity']

    # Create order history entries
    for item in request.cart_items:
        order = OrderHistory(
            user_id=request.user_id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            order_date=datetime.now().isoformat(),
            status='pending'
        )
        db.add(order)
        # Update product stock
        product.stock -= item['quantity']
    
    db.commit()
    
    return {"message": "Order created successfully", "total_amount": total_amount}

def include_router(app):
    app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI
    
    app = FastAPI()
    include_router(app)
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # Ensure the static directory exists for serving static files
    import os
    static_dir = "static"
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
