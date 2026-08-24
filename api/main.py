from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import Product, OrderHistory
from database import get_db

app = FastAPI()
router = APIRouter()

@router.get("/products")
def get_products(category: str = None, search: str = None, db: Session = Depends(get_db)):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category == category)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    products = query.all()
    return products

@router.get("/orders")
def get_order_history(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(OrderHistory).filter(OrderHistory.user_id == user_id).all()
    return orders

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)