from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.models import Expense
from database import get_db

router = APIRouter()

@router.get("/dashboard")
def get_dashboard(user_id: int, db: Session = Depends(get_db)):
    total_spent = 0
    category_breakdown = {}

    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    
    for expense in expenses:
        total_spent += expense.amount
        if expense.category in category_breakdown:
            category_breakdown[expense.category] += expense.amount
        else:
            category_breakdown[expense.category] = expense.amount

    return {
        "total_spent": total_spent,
        "category_breakdown": category_breakdown
    }

from fastapi import FastAPI
app = FastAPI()
app.include_router(router)
