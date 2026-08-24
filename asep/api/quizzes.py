from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from asep.db.models import Quiz, User, Question
from asep.db.database import get_db
from pydantic import BaseModel
from uuid import UUID

router = APIRouter()

class QuizCreate(BaseModel):
    title: str
    questions: list

@router.post("/quizzes/", response_model=Quiz)
def create_quiz(quiz: QuizCreate, teacher_id: UUID, db: Session = Depends(get_db)):
    # Check if the teacher exists
    teacher = db.query(User).filter(User.id == teacher_id, User.role == 'teacher').first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    new_quiz = Quiz(title=quiz.title, questions=quiz.questions, teacher_id=teacher_id)
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)

    return new_quiz

@router.get("/quizzes/{quiz_id}", response_model=Quiz)
def read_quiz(quiz_id: UUID, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.get("/quizzes/")
def list_quizzes(db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).all()
    return quizzes

@router.put("/quizzes/{quiz_id}", response_model=Quiz)
def update_quiz(quiz_id: UUID, quiz: QuizCreate, db: Session = Depends(get_db)):
    existing_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not existing_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    existing_quiz.title = quiz.title
    existing_quiz.questions = quiz.questions
    db.commit()
    db.refresh(existing_quiz)

    return existing_quiz

@router.delete("/quizzes/{quiz_id}", response_model=dict)
def delete_quiz(quiz_id: UUID, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    db.delete(quiz)
    db.commit()

    return {"detail": "Quiz deleted successfully"}

def include_router(app):
    app.include_router(router)