from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))


from sqlalchemy.orm import sessionmaker
from db.database import get_db, Base  # Ensure the correct import path is used

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_checkout_integration.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
