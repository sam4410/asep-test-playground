import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from api.main import app  # Adjusted import to use the correct path
