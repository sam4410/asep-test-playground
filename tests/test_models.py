import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from db.models import Quiz, Question, Answer
from models import Quiz, Question, Answer

# ... rest of the test code ...
