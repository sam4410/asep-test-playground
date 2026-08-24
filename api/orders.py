from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import OrderHistory
from database import get_db

router = APIRouter()

@router.get("/orders")
def get_order_history(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(OrderHistory).filter(OrderHistory.user_id == user_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return orders

def include_router(app):
    app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI
    
    app = FastAPI()
    include_router(app)
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # Ensure the static directory exists
    import os
    if not os.path.exists("static"):
        os.makedirs("static")
