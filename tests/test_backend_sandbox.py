from fastapi.testclient import TestClient
from api.dashboard import router as include_router  # Ensure correct import path
client = TestClient(include_router)
# Define your test cases here
app.include_router(router)