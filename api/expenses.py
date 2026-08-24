from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.models import Expense
from database import get_db  # Assuming you have a database module for session management

router = APIRouter()

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    date: str  # Consider using a date type if you want to enforce date format
    user_id: int

@router.post("/expenses/", status_code=201)  # Set status code for successful creation
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = Expense(
        amount=expense.amount,
        category=expense.category,
        date=expense.date,
        user_id=expense.user_id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.get("/expenses/category/")
def get_expenses_by_category(category: str, db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.category == category).all()
    return {"expenses": expenses}  # Return a dictionary for consistency

@router.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    return {"detail": exc.detail}  # Customize your error response as needed
