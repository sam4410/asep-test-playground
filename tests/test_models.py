from api.models import Quiz, Question, Answer, Habit  # Adjusted import to include Habit
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from db.models import Quiz, Question, Answer
from models import Quiz, Question, Answer

# ... rest of the test code ...
