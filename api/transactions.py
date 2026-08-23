from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.models import Expense
from database import get_db
from datetime import datetime

router = APIRouter()

class ExpenseCreate(BaseModel):
    amount: int  # Store amounts as integer cents
    category: str
    date: str
    user_id: int

class ExpenseUpdate(BaseModel):
    amount: int
    category: str
    date: str

@router.post("/expenses", response_model=ExpenseCreate)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = Expense(amount=expense.amount, category=expense.category, date=expense.date, user_id=expense.user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.get("/expenses/{expense_id}", response_model=ExpenseCreate)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense

@router.put("/expenses/{expense_id}", response_model=ExpenseCreate)
def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db_expense.amount = expense.amount
    db_expense.category = expense.category
    db_expense.date = expense.date
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(db_expense)
    db.commit()
    return {"detail": "Expense deleted successfully"}

@router.get("/expenses", response_model=list[ExpenseCreate])
def get_expenses(category: str = None, start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    query = db.query(Expense)

    if category:
        query = query.filter(Expense.category == category)

    if start_date:
        query = query.filter(Expense.date >= start_date)

    if end_date:
        query = query.filter(Expense.date <= end_date)

    expenses = query.all()

    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found")

    return expenses

@router.get("/expenses/user/{user_id}", response_model=list[ExpenseCreate])
def get_expenses_by_user(user_id: int, db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found for this user")
    return expenses
