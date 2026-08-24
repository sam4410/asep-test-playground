from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import Task, User
from db.database import get_db
from pydantic import BaseModel
from uuid import UUID

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: str
    assignee: str
    due_date: str  # Consider using a date type for better validation
    status: str  # Should be validated against allowed values

@router.post("/tasks/", response_model=dict)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Check if the assignee exists
    assignee = db.query(User).filter(User.username == task.assignee).first()
    if not assignee:
        raise HTTPException(status_code=404, detail="Assignee not found")

    new_task = Task(
        title=task.title,
        description=task.description,
        assignee=assignee.id,  # Use the user's ID instead of username
        due_date=task.due_date,
        status=task.status
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": "Task created successfully", "task_id": str(new_task.id)}

@router.get("/tasks/", response_model=list)
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return [{"task_id": str(task.id), "title": task.title, "description": task.description, 
             "assignee": task.assignee, "due_date": task.due_date, "status": task.status} for task in tasks]

@router.get("/tasks/{task_id}", response_model=dict)
def get_task(task_id: UUID, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": str(task.id), "title": task.title, "description": task.description, 
            "assignee": task.assignee, "due_date": task.due_date, "status": task.status}

from fastapi import APIRouter
from asep.api.quizzes import router as quizzes_router
from asep.api.expenses import router as expenses_router

router.include_router(quizzes_router, prefix="/quizzes", tags=["quizzes"])
router.include_router(expenses_router, prefix="/expenses", tags=["expenses"])