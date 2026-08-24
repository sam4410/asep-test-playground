from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.models import Budget  # Assuming you have a Budget model
from database import get_db

router = APIRouter()

class BudgetCreate(BaseModel):
    category: str
    monthly_budget: int  # Store amounts as integer cents

class BudgetUpdate(BaseModel):
    monthly_budget: int = None

@router.post("/budgets/", response_model=BudgetCreate)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    db_budget = Budget(
        category=budget.category,
        monthly_budget=budget.monthly_budget
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

@router.put("/budgets/{category}", response_model=BudgetUpdate)
def update_budget(category: str, budget: BudgetUpdate, db: Session = Depends(get_db)):
    db_budget = db.query(Budget).filter(Budget.category == category).first()
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    if budget.monthly_budget is not None:
        db_budget.monthly_budget = budget.monthly_budget

    db.commit()
    db.refresh(db_budget)
    return db_budget

@router.get("/budgets/{category}")
def get_budget(category: str, db: Session = Depends(get_db)):
    db_budget = db.query(Budget).filter(Budget.category == category).first()
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return db_budget

@router.get("/budgets/")
def get_all_budgets(db: Session = Depends(get_db)):
    budgets = db.query(Budget).all()
    return {"budgets": budgets}

def include_router(app):
    app.include_router(router, prefix="/api/v1")

import sys
sys.path.append("..")  # Adjust the path to include the parent directory