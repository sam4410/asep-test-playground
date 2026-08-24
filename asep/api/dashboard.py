from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from asep.db.models import QuizSubmission, User
from asep.db.database import get_db
from uuid import UUID

router = APIRouter()

@router.get("/dashboard/{teacher_id}", response_model=dict)
def get_teacher_dashboard(teacher_id: UUID, db: Session = Depends(get_db)):
    # Check if the teacher exists
    teacher = db.query(User).filter(User.id == teacher_id, User.role == 'teacher').first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    # Get all quiz submissions for the teacher's quizzes
    submissions = db.query(QuizSubmission).join(QuizSubmission.quiz).filter(QuizSubmission.quiz.has(teacher_id=teacher_id)).all()

    # Prepare the dashboard data
    dashboard_data = {}
    for submission in submissions:
        student_id = submission.student_id
        if student_id not in dashboard_data:
            dashboard_data[student_id] = []
        dashboard_data[student_id].append({
            "quiz_id": submission.quiz_id,
            "score": submission.score,  # Assuming score is stored in QuizSubmission
            "submitted_at": submission.submitted_at
        })

    return {"student_scores": dashboard_data}

def include_router(app):
    app.include_router(router, prefix="/api/v1", tags=["dashboard"])

__all__ = ["router", "include_router"]
