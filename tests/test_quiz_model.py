import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # Ensure correct path
from api.main import app  # Adjusted import to use the correct path
from fastapi.testclient import TestClient
client = TestClient(app)
def test_example():
    assert True
@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_quiz(db):
    quiz = Quiz(title="Sample Quiz")
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    assert quiz.id is not None
    assert quiz.title == "Sample Quiz"

def test_create_question(db):
    quiz = Quiz(title="Sample Quiz")
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    question = Question(text="What is 2 + 2?", quiz_id=quiz.id)
    db.add(question)
    db.commit()
    db.refresh(question)
    assert question.id is not None
    assert question.text == "What is 2 + 2?"
    assert question.quiz_id == quiz.id

def test_create_answer(db):
    quiz = Quiz(title="Sample Quiz")
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    question = Question(text="What is 2 + 2?", quiz_id=quiz.id)
    db.add(question)
    db.commit()
    db.refresh(question)

    answer = Answer(text="4", question_id=question.id)
    db.add(answer)
    db.commit()
    db.refresh(answer)
    assert answer.id is not None
    assert answer.text == "4"
    assert answer.question_id == question.id

def test_quiz_not_found(db):
    quiz = db.query(Quiz).filter(Quiz.id == 999).first()
    assert quiz is None

def test_question_not_found(db):
    question = db.query(Question).filter(Question.id == 999).first()
    assert question is None

def test_answer_not_found(db):
    answer = db.query(Answer).filter(Answer.id == 999).first()
    assert answer is None
    answer = Answer(text="4", question_id=question.id)
    db.add(answer)
    db.commit()
    db.refresh(answer)
    assert answer.id is not None
    assert answer.text == "4"
    assert answer.question_id == question.id

def test_quiz_not_found(db):
    quiz = db.query(Quiz).filter(Quiz.id == 999).first()
    assert quiz is None

def test_question_not_found(db):
    question = db.query(Question).filter(Question.id == 999).first()
    assert question is None

def test_answer_not_found(db):
    answer = db.query(Answer).filter(Answer.id == 999).first()
    assert answer is None
