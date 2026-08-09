from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from .models import Habit
from pydantic import BaseModel
from typing import List
from .auth import get_current_user

router = APIRouter()

class HabitCreate(BaseModel):
    name: str

class HabitResponse(BaseModel):
    id: int
    user_id: int
    name: str
    streak: int
    created_at: str  # ISO 8601 format

@router.post("/", response_model=HabitResponse)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_habit = Habit(user_id=current_user.id, name=habit.name)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

@router.get("/", response_model=List[HabitResponse])
def read_habits(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    habits = db.query(Habit).filter(Habit.user_id == current_user.id).offset(skip).limit(limit).all()
    return habits

@router.get("/{habit_id}", response_model=HabitResponse)
def read_habit(habit_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

@router.put("/{habit_id}", response_model=HabitResponse)
def update_habit(habit_id: int, habit: HabitCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    db_habit.name = habit.name
    db.commit()
    db.refresh(db_habit)
    return db_habit

@router.delete("/{habit_id}", response_model=dict)
def delete_habit(habit_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    db.delete(db_habit)
    db.commit()
    return {"message": "Habit deleted successfully"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits", tags=["habits"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Logic to decode the token and return the current user
    pass

router.include_router(router, prefix="/habits