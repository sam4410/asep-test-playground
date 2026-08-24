from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from asep.db.models import Quiz, QuizSubmission, User, Question
from asep.db.database import get_db
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Dict

router = APIRouter()

class QuizCreate(BaseModel):
    title: str
    questions: List[Dict[str, str]]  # Specify the structure of questions

class QuizSubmissionCreate(BaseModel):
    quiz_id: UUID
    student_id: UUID
    answers: Dict[UUID, str]  # Mapping of question_id to answer

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

@router.post("/quizzes/submit/", response_model=dict)  # Change response model to dict
def submit_quiz(submission: QuizSubmissionCreate, db: Session = Depends(get_db)):
    # Check if the quiz exists
    quiz = db.query(Quiz).filter(Quiz.id == submission.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Check if the student exists
    student = db.query(User).filter(User.id == submission.student_id, User.role == 'student').first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Calculate score
    score = 0
    for question_id, answer in submission.answers.items():
        question = db.query(Question).filter(Question.id == question_id).first()
        if question and question.correct_answer == answer:
            score += 1

    # Save the submission
    new_submission = QuizSubmission(
        quiz_id=submission.quiz_id,
        student_id=submission.student_id,
        answers=submission.answers,
        score=score,  # Store the calculated score
        submitted_at=datetime.utcnow()
    )
    db.add(new_submission)
    db.commit()

    return {"submission_id": new_submission.id, "score": score}  # Return submission_id instead of the whole object

@router.get("/quizzes/submit/{submission_id}", response_model=QuizSubmission)
def get_quiz_submission(submission_id: UUID, db: Session = Depends(get_db)):
    submission = db.query(QuizSubmission).filter(QuizSubmission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission

@router.get("/quizzes/")
def list_quizzes(db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).all()
    return quizzes

@router.get("/quizzes/{quiz_id}", response_model=Quiz)
def read_quiz(quiz_id: UUID, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz
