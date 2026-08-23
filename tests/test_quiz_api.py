import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # Ensure correct path
from api.main import app  # Adjusted import to use the correct path
from fastapi.testclient import TestClient
client = TestClient(app)
def test_example():
    assert True
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

def test_take_quiz(db):
    quiz = Quiz(title="Sample Quiz")
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    question = Question(text="What is 2 + 2?", quiz_id=quiz.id, correct_answer_id=None)
    db.add(question)
    db.commit()
    db.refresh(question)

    answer = Answer(text="4", question_id=question.id)
    db.add(answer)
    db.commit()
    db.refresh(answer)

    response = client.post(f"/api/v1/quizzes/{quiz.id}/take", json={
        "answers": [
            {
                "question_id": question.id,
                "selected_answer_id": answer.id
            }
        ]
    })
    assert response.status_code == 200
    assert response.json()["score"] == 1

def test_take_quiz_invalid_question(db):
    quiz = Quiz(title="Sample Quiz")
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    response = client.post(f"/api/v1/quizzes/{quiz.id}/take", json={
        "answers": [
            {
                "question_id": 999,  # Invalid question ID
                "selected_answer_id": 1
            }
        ]
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Question 999 not found"
    assert response.status_code == 200
    assert response.json() == {"detail": "Quiz deleted successfully"}

    response = client.get(f"/api/v1/quizzes/{quiz.id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Quiz not found"
