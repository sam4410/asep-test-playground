import pytest
from fastapi.testclient import TestClient
from asep.api.main import app
from asep.db.database import get_db
from asep.db.models import Quiz, QuizSubmission, User
from uuid import uuid4

    pass
def create_teacher(db):
    teacher = User(id=uuid4(), username="teacher1", password="password", role="teacher")
    db.add(teacher)
