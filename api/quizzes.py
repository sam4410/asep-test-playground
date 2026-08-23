from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import Quiz, Question, Answer  # Adjusted import to use relative path
from .database import get_db  # Adjusted import to use relative path
from pydantic import BaseModel
from typing import List

router = APIRouter()

        db_answer = Answer(text=question.correct_answer.text, question_id=db_question.id)
class AnswerCreate(BaseModel):
    text: str

class QuestionCreate(BaseModel):
    text: str
    correct_answer: AnswerCreate

class QuizCreate(BaseModel):
    title: str
    questions: List[QuestionCreate]  # Changed to List for better type hinting

@router.post("/api/v1/quizzes", response_model=Quiz)
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):
    db_quiz = Quiz(title=quiz.title)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)

@router.get("/api/v1/quizzes/{quiz_id}", response_model=Quiz)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz

@router.put("/api/v1/quizzes/{quiz_id}", response_model=Quiz)
def update_quiz(quiz_id: int, quiz: QuizCreate, db: Session = Depends(get_db)):
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    db_quiz.title = quiz.title
    db.commit()
    db.refresh(db_quiz)

    # Update questions and answers logic can be added here

    return db_quiz

@router.delete("/api/v1/quizzes/{quiz_id}", response_model=dict)
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    db.delete(db_quiz)
    db.commit()
    return {"detail": "Quiz deleted successfully"}
