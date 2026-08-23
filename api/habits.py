from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import Habit, User  # Adjusted import to be relative
from database import get_db
from pydantic import BaseModel

router = APIRouter()

class HabitCreate(BaseModel):
    name: str
    target_frequency: int  # Frequency in days

@router.post("/habits")
def create_habit(habit: HabitCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_habit = Habit(name=habit.name, target_frequency=habit.target_frequency, user_id=user.id)
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return {"id": new_habit.id, "name": new_habit.name, "target_frequency": new_habit.target_frequency}

def get_current_user():
    # Placeholder for user authentication logic
    pass

@router.get("/habits")
def get_habits(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Habit).filter(Habit.user_id == user.id).all()

@router.get("/habits/{habit_id}")
def get_habit(habit_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

@router.get("/habits/streak/{habit_id}")
def get_habit_streak(habit_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return {"habit_id": habit.id, "streak_count": habit.streak_count}
    return {"habit_id": habit.id, "streak_count": habit.streak_count}
def get_current_user():
    # Placeholder for user authentication logic
    pass

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import Habit
from database import get_db

router = APIRouter()

@router.post("/habits/log")
def log_habit(habit_name: str, user_id: int, db: Session = Depends(get_db)):
    habit = Habit(name=habit_name, user_id=user_id)
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return {"id": habit.id, "name": habit.name, "streak_count": habit.streak_count, "user_id": habit.user_id}

@router.get("/habits")
def get_habits(user_id: int, db: Session = Depends(get_db)):
    habits = db.query(Habit).filter(Habit.user_id == user_id).all()
    return habits

from fastapi import FastAPI
app = FastAPI()
app.include_router(router)