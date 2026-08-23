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