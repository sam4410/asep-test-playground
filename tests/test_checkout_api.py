from .api.main import app  # Adjusted import to use relative path

# Your test code here
sys.path.append(str(Path(__file__).resolve().parent.parent))

from api.main import app  # Adjusted import to use the correct path
