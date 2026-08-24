from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import HabitModel
from db.database import get_db
from pydantic import BaseModel
from fastapi import APIRouter
from datetime import datetime

app = FastAPI()
router = APIRouter()

class HabitLog(BaseModel):
    user_id: str
    habit_name: str
    log_date: datetime = None

@router.post("/habits/log")
def log_habit(habit: HabitLog, db: Session = Depends(get_db)):
    if habit.log_date is None:
        habit.log_date = datetime.utcnow()
    new_habit = HabitModel(user_id=habit.user_id, habit_name=habit.habit_name, log_date=habit.log_date)
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return {"id": new_habit.id, "user_id": new_habit.user_id, "habit_name": new_habit.habit_name, "log_date": new_habit.log_date}

@router.get("/habits/")
def get_habits(user_id: str, db: Session = Depends(get_db)):
    habits = db.query(HabitModel).filter(HabitModel.user_id == user_id).all()
    if not habits:
        raise HTTPException(status_code=404, detail="No habits found for this user")
    return habits

app.include_router(router, prefix="/api")