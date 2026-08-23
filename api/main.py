from fastapi import FastAPI, Depends, HTTPException, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.models import User, get_db

app = FastAPI()
router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str

class UserRetrieve(BaseModel):
    id: int
    username: str

@router.post("/signup", response_model=UserRetrieve)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(username=user.username, password=user.password)  # Password should be hashed in production
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
@router.post("/expenses", response_model=ExpenseRetrieve)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = Expense(amount=expense.amount, category=expense.category, date=expense.date, user_id=expense.user_id)
    db.add(db_expense)
    db.commit()  # Commit the transaction to save the expense
    db.refresh(db_expense)
    return db_expense
    return expenses
