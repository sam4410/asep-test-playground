from .api.main import app  # Adjusted import to use relative path

# Your test code here
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from api.main import app  # Adjusted import to use the correct path
