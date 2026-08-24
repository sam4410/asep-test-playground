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

