from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import Task, User  # Use relative import
from .database import get_db  # Use relative import
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

@router.get("/tasks/user/{user_id}", response_model=list[Task])
def get_user_tasks(user_id: UUID, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.assignee_id == user_id).all()
    return tasks

@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"detail": "Task deleted successfully"}

class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    status: str = None
    assignee_id: UUID = None

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.status is not None:
        task.status = task_update.status
    if task_update.assignee_id is not None:
        task.assignee_id = task_update.assignee_id

    db.commit()
    db.refresh(task)

    return task

from fastapi import FastAPI
app = FastAPI()
app.include_router(router, prefix="/api")

import os
static_dir = "static"
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")
