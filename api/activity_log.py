from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import ActivityLog, Task
from db.database import get_db
from pydantic import BaseModel
from uuid import UUID

router = APIRouter()

class ActivityLogEntry(BaseModel):
    task_id: UUID
    action: str
    timestamp: str  # Consider using a datetime type for better validation

@router.post("/activity_log/", response_model=dict)
def create_activity_log(entry: ActivityLogEntry, db: Session = Depends(get_db)):
    # Check if the task exists
    task = db.query(Task).filter(Task.id == entry.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    new_log = ActivityLog(
        task_id=entry.task_id,
        action=entry.action,
        timestamp=entry.timestamp
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return {"message": "Activity log entry created successfully", "log_id": str(new_log.id)}

@router.get("/activity_log/", response_model=list)
def get_activity_log(db: Session = Depends(get_db)):
    logs = db.query(ActivityLog).all()
    return [{"log_id": str(log.id), "task_id": log.task_id, "action": log.action, 
             "timestamp": log.timestamp} for log in logs]

from fastapi import APIRouter
router.include_router(router)
