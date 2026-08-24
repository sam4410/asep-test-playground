from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import Product
from database import get_db

router = APIRouter()

@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Product.category).distinct().all()
    return [category[0] for category in categories]

@router.get("/products/search")
def search_products(query: str, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.name.ilike(f"%{query}%")).all()
    return products

from fastapi import FastAPI
from . import router  # Corrected import for the router
app = FastAPI()
app.include_router(router, prefix="/api/v1")