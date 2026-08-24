from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import Task, User
from db.database import get_db
from pydantic import BaseModel
from uuid import UUID

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: str = None
    assignee_id: UUID = None

@router.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        status='pending',  # Default status
        assignee_id=task.assignee_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get("/tasks/")
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: UUID, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
class TaskAssign(BaseModel):
    assignee_id: UUID

@router.post("/tasks/{task_id}/assign/", response_model=Task)
def assign_task(task_id: UUID, task_assign: TaskAssign, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.assignee_id = task_assign.assignee_id
    db.commit()
    db.refresh(task)

    return task

from fastapi import FastAPI
app = FastAPI()
app.include_router(router, prefix="/api")

import os
if not os.path.exists("static"):
    os.makedirs("static")