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
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username, User.password == user.password).first()  # Password should be hashed in production
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

app.include_router(router)
