from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from asep.api.middleware import require_role
from asep.api.routes import router as api_router
from asep.api.middleware.auth import get_current_user
    """Endpoint to fetch the current user's JWT payload."""
    return {"user_id": payload.get("sub"), "roles": payload.get("roles", [])}
app = FastAPI()

# Include API router
# All regular API endpoints require at least a \"user\" role.
# Specific endpoints can override this with their own Depends(require_role(...))
app.include_router(api_router, prefix="/api/v1", dependencies=[Depends(require_role("user"))])

# Health check endpoint
