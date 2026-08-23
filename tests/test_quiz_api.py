import pytest
from fastapi.testclient import TestClient
from main import app  # Adjusted import to use the correct path
from db.models import Quiz, Question, Answer
from db.database import get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    # Setup the database for testing
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_quiz(db):
    response = client.post("/api/v1/quizzes", json={
        "title": "Sample Quiz",
        "questions": [
            {
                "text": "What is 2 + 2?",
                "correct_answer": {"text": "4"}
            }
        ]
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Sample Quiz"

def test_get_quiz(db):
    quiz = Quiz(title="Sample Quiz")
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    response = client.get(f"/api/v1/quizzes/{quiz.id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Sample Quiz"

def test_update_quiz(db):
    quiz = Quiz(title="Sample Quiz")
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    response = client.put(f"/api/v1/quizzes/{quiz.id}", json={
        "title": "Updated Quiz",
        "questions": []
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Quiz"

def test_delete_quiz(db):
    quiz = Quiz(title="Sample Quiz")
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    response = client.delete(f"/api/v1/quizzes/{quiz.id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Quiz deleted successfully"}

    response = client.get(f"/api/v1/quizzes/{quiz.id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Quiz not found"
