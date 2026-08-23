import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from db.database import get_db, Base  # Ensure the correct import path is used
