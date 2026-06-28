from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from asep.api.middleware import require_role
from asep.api.routes import router as api_router
def list_projects(user=Depends(require_role("admin"))) -> list[dict]:
    # Mock projects endpoint, only accessible by admin users
    return [{"id": 1, "name": "ASEP Platform", "status": "running"}]


@app.get("/api/v1/projects")
def list_projects() -> list[dict]:
    # Mock projects endpoint
    return [{"id": 1, "name": "ASEP Platform", "status": "running"}]
app.include_router(api_router, prefix="/api/v1")

# Health check endpoint
