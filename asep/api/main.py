import os  # Added import for os to check static directory existence
import pytest
from fastapi.testclient import TestClient
from asep.api.main import app  # Adjusted import statement to reflect the correct module path
import os  # Added import for os module
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
@app.get("/api/v1/projects")
def list_projects() -> list[dict]:
    # Mock projects endpoint
    return [{"id": 1, "name": "ASEP Platform", "status": "running"}]
import os  # Added import for os module
# Ensure the static directory exists
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")  # Changed mount path to "/static" to avoid conflict with API routesapp = FastAPI()

# Ensure the static directory exists before mounting
if not os.path.exists("static"):  # Check for static directory existence
    os.makedirs("static")  # Create the directory if it doesn't exist

app = FastAPI()

# Serve static files from the 'public' directory
app.mount("/", StaticFiles(directory="public", html=True), name="static")

# Other app configurations and routes...
