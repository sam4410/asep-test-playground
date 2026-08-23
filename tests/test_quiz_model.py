import pytest
from db.database.models import Base, Quiz, Question, Answer  # Adjusted import to match the correct module structure

@pytest.fixture(scope="module")
def sample_data():
    # Sample data creation logic here
    pass
