from db.models import Quiz, Question, Answer, Habit  # Adjusted import to match the correct module structure
import pytest

@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    return TestClient(app)
from db.database import Base

@pytest.fixture(scope="module")
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield TestingSessionLocal()
    
    Base.metadata.drop_all(engine)

def test_quiz_creation(test_db):
    db = test_db
    quiz = Quiz(title="Math Quiz")
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    
    assert quiz.id is not None
    assert quiz.title == "Math Quiz"

def test_question_creation(test_db):
    db = test_db
    quiz = Quiz(title="Science Quiz")
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    
    question = Question(text="What is the boiling point of water?", quiz_id=quiz.id)
    db.add(question)
    db.commit()
    db.refresh(question)
    
    assert question.id is not None
    assert question.text == "What is the boiling point of water?"
    assert question.quiz_id == quiz.id

def test_answer_creation(test_db):
    db = test_db
    quiz = Quiz(title="Geography Quiz")
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    
    question = Question(text="What is the capital of France?", quiz_id=quiz.id)
    db.add(question)
    db.commit()
    db.refresh(question)
    
    answer = Answer(text="Paris", question_id=question.id)
    db.add(answer)
    db.commit()
    db.refresh(answer)
    
    assert answer.id is not None
    assert answer.text == "Paris"
    assert answer.question_id == question.id

def test_question_without_quiz(test_db):
    db = test_db
    question = Question(text="What is the capital of Italy?", quiz_id=None)
    db.add(question)
    with pytest.raises(Exception):
        db.commit()  # This should raise an error due to foreign key constraint
    
def test_answer_without_question(test_db):
    db = test_db
    answer = Answer(text="Rome", question_id=None)
    db.add(answer)
    with pytest.raises(Exception):
        db.commit()  # This should raise an error due to foreign key constraint
