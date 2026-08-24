from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.models import Transaction
from db.database import get_db

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_data(db: Session = Depends(get_db)):
    total_spent = db.query(func.sum(Transaction.amount)).filter(Transaction.date >= '2023-10-01').scalar() or 0
    category_breakdown = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label('total')
    ).filter(Transaction.date >= '2023-10-01').group_by(Transaction.category).all()

    breakdown_dict = {category: total for category, total in category_breakdown}

    return {
        "total_spent": total_spent,
        "category_breakdown": breakdown_dict
    }

def include_router(app):
    app.include_router(router, prefix="/api/v1")