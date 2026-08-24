from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..models import Transaction  # Corrected import to use relative path
from ..database import get_db  # Corrected import to use relative path

router = APIRouter()

class TransactionCreate(BaseModel):
    amount: int  # Store amounts as integer cents
    category: str
    date: str  # Use ISO format for date
    note: str = None

class TransactionUpdate(BaseModel):
    amount: int = None
    category: str = None
    date: str = None
    note: str = None

@router.post("/transactions", response_model=TransactionCreate)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.put("/transactions/{transaction_id}", response_model=TransactionCreate)
def update_transaction(transaction_id: int, transaction: TransactionUpdate, db: Session = Depends(get_db)):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in transaction.dict(exclude_unset=True).items():
        setattr(db_transaction, key, value)

    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(db_transaction)
    db.commit()
    return {"detail": "Transaction deleted successfully"}

@router.get("/transactions")
def get_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).offset(skip).limit(limit).all()
    return transactions

@router.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction