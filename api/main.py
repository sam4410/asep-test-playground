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
