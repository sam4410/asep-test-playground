from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.db.models import Task, User  # Adjusted import to use the correct path
from api.db.database import get_db  # Adjusted import to use the correct path
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: str
    assignee_id: int

@router.post("/api/v1/tasks", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Validate assignee exists
    assignee = db.query(User).filter(User.id == task.assignee_id).first()
    if not assignee:
        raise HTTPException(status_code=404, detail="Assignee not found")
    
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

from api.main import app  # No change needed here
app.include_router(router)
