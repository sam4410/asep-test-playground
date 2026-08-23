from fastapi import FastAPI, Depends, HTTPException, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .db.models import Team, User, get_db

app = FastAPI()
router = APIRouter()

app = FastAPI()
router = APIRouter()

@router.get("/api/v1/products", response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

class CategoryCreate(BaseModel):
    name: str
    user_id: int

@router.post("/categories", response_model=CategoryCreate)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    if not category.name:
        raise HTTPException(status_code=422, detail="Category name cannot be empty")
    db_category = Category(name=category.name, user_id=category.user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/categories", response_model=list[CategoryCreate])
@router.get("/api/v1/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
    
app.include_router(router)
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories

app.include_router(router)

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    date: str
    user_id: int

@router.post("/expenses", response_model=ExpenseCreate)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = Expense(amount=expense.amount, category=expense.category, date=expense.date, user_id=expense.user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

app.include_router(router)
app = FastAPI()
router = APIRouter()

@router.get("/api/v1/products", response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

app.include_router(router)
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.models import Expense
from database import get_db

app = FastAPI()
router = APIRouter()

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    date: str
    user_id: int

@router.post("/expenses", response_model=ExpenseCreate)
def create_expense(expense: ExpenseCreate, db: Session = next(get_db())):
    db_expense = Expense(amount=expense.amount, category=expense.category, date=expense.date, user_id=expense.user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

app.include_router(router)
