from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import Product
from database import get_db
from pydantic import BaseModel

router = APIRouter()

class ProductCreate(BaseModel):
    name: str
    description: str = None
    price: float
    category: str
    image_url: str = None
    stock: int

class ProductUpdate(BaseModel):
    name: str = None
    description: str = None
    price: float = None
    category: str = None
    image_url: str = None
    stock: int = None

@router.post("/products", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/products", response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.get("/stock", response_model=dict)
def get_stock_levels(db: Session = Depends(get_db)):
    stock_levels = db.query(Product.name, Product.stock).all()
    return {name: stock for name, stock in stock_levels}

def include_router(app):
    app.include_router(router, prefix="/api/v1/admin")

if __name__ == "__main__":
    import uvicorn
    from api.main import app  # Corrected import statement
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

include_router(app)
