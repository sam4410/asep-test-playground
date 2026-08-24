from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import User
from db.database import get_db
from pydantic import EmailStr
from pydantic import BaseModel
from passlib.context import CryptContext


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, password=hashed_password, email=user.email)
    db.add(db_user)
    username: str
    password: str

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return {"id": db_user.id, "username": db_user.username}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Username and password are required")
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"id": db_user.id, "username": db_user.username}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Login successful", "username": db_user.username, "id": db_user.id}


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}

@router.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.password = pwd_context.hash(user.password)
    db.commit()
    return {"id": db_user.id, "username": db_user.username}
