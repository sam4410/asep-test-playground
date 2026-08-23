from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import Quiz, Question, Answer
from db.database import get_db
from pydantic import BaseModel

router = APIRouter()

class AnswerCreate(BaseModel):
    text: str

class QuestionCreate(BaseModel):
    text: str
    correct_answer: AnswerCreate

class QuizCreate(BaseModel):
    title: str
    questions: list[QuestionCreate]

@router.post("/api/v1/quizzes", response_model=Quiz)
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):
    db_quiz = Quiz(title=quiz.title)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)

    for question in quiz.questions:
        db_question = Question(text=question.text, quiz_id=db_quiz.id)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        db_answer = Answer(text=question.correct_answer.text, question_id=db_question.id)
        db.add(db_answer)
        db.commit()
        db.refresh(db_answer)


    return db_quiz

from fastapi import FastAPI
app = FastAPI()
app.include_router(router)