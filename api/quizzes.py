from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import Quiz, Question, Answer  # Adjusted import to use relative path
from .database import get_db  # Adjusted import to use relative path
from pydantic import BaseModel

router = APIRouter()

class AnswerSubmission(BaseModel):
    question_id: int
    selected_answer_id: int

class QuizSubmission(BaseModel):
    answers: list[AnswerSubmission]

@router.post("/api/v1/quizzes/{quiz_id}/take")
def take_quiz(quiz_id: int, submission: QuizSubmission, db: Session = Depends(get_db)):
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    score = 0
    for answer in submission.answers:
        db_question = db.query(Question).filter(Question.id == answer.question_id).first()
        if not db_question:
            raise HTTPException(status_code=404, detail=f"Question {answer.question_id} not found")

        correct_answer = db.query(Answer).filter(Answer.id == db_question.correct_answer_id).first()
        if correct_answer and correct_answer.id == answer.selected_answer_id:
            score += 1

    return {"quiz_id": quiz_id, "score": score}

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