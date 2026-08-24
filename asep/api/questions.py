from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from asep.db.models import Question, Quiz
from asep.db.database import get_db
from pydantic import BaseModel
from uuid import UUID

router = APIRouter()

class QuestionCreate(BaseModel):
    question_text: str
    question_type: str  # e.g., 'multiple_choice', 'true_false', etc.
    options: list = None  # Store options as a list
    correct_answer: str
    quiz_id: UUID

@router.post("/questions/", response_model=Question)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    new_question = Question(
        question_text=question.question_text,
        question_type=question.question_type,
        options=','.join(question.options) if question.options else None,
        correct_answer=question.correct_answer,
        quiz_id=question.quiz_id
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question

@router.get("/questions/{question_id}", response_model=Question)
def read_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.get("/questions/")
def list_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    return questions

@router.put("/questions/{question_id}", response_model=Question)
def update_question(question_id: int, question: QuestionCreate, db: Session = Depends(get_db)):
    existing_question = db.query(Question).filter(Question.id == question_id).first()
    if not existing_question:
        raise HTTPException(status_code=404, detail="Question not found")

    existing_question.question_text = question.question_text
    existing_question.question_type = question.question_type
    existing_question.options = ','.join(question.options) if question.options else None
    existing_question.correct_answer = question.correct_answer
    db.commit()
    db.refresh(existing_question)

    return existing_question

@router.delete("/questions/{question_id}", response_model=dict)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(question)
    db.commit()

    return {"detail": "Question deleted successfully"}

def include_router(app):  # Ensure this function is included in the correct module
    app.include_router(router)  # No prefix added to avoid conflicts with existing routes
