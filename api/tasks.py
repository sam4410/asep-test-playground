from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import Task
from db.database import get_db
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: str
    assignee_id: int

@router.post("/api/v1/tasks", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(
        title=task.title,
        description=task.description,
        assignee_id=task.assignee_id,
        status="todo",  # Default status
        created_at=int(datetime.now().timestamp()),  # Store as Unix timestamp
        updated_at=int(datetime.now().timestamp())   # Store as Unix timestamp
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

from main import app  # Adjusted import to match the correct module structure
app.include_router(router)
