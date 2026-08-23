from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.models import Budget
from database import get_db

router = APIRouter()

class BudgetCreate(BaseModel):
    category: str
    amount: int  # Store budget amounts as integer cents
    user_id: int

class BudgetUpdate(BaseModel):
    amount: int

@router.post("/budgets", response_model=BudgetCreate)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    db_budget = Budget(category=budget.category, amount=budget.amount, user_id=budget.user_id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

@router.get("/budgets/{user_id}", response_model=list[BudgetCreate])
def get_budgets(user_id: int, db: Session = Depends(get_db)):
    budgets = db.query(Budget).filter(Budget.user_id == user_id).all()
    return budgets

@router.put("/budgets/{budget_id}", response_model=BudgetCreate)
def update_budget(budget_id: int, budget: BudgetUpdate, db: Session = Depends(get_db)):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if db_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    db_budget.amount = budget.amount
    db.commit()
    db.refresh(db_budget)
    return db_budget

@router.delete("/budgets/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if db_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    db.delete(db_budget)
    db.commit()
    return {"detail": "Budget deleted successfully"}

from fastapi import FastAPI
app = FastAPI()
app.include_router(router)

@app.get("/budgets/check/{user_id}")
def check_budget(user_id: int, db: Session = Depends(get_db)):
    budgets = db.query(Budget).filter(Budget.user_id == user_id).all()
    total_spent = sum(budget.amount for budget in budgets)
    return {"total_spent": total_spent}

@app.get("/budgets/status/{user_id}")
def budget_status(user_id: int, db: Session = Depends(get_db)):
    budgets = db.query(Budget).filter(Budget.user_id == user_id).all()
    return {"budgets": budgets}

import sys
sys.path.append("..")  # Add parent directory to path for module resolution
