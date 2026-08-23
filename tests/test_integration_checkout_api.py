from .api.main import app  # Adjusted import to use relative path

# Your test code here
sys.path.append(str(Path(__file__).resolve().parent.parent))

from db.database import get_db, Base  # Ensure the correct import path is used
