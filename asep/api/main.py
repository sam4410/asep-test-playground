from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from asep.api.middleware import require_role
from asep.api.routes import router as api_router
from asep.api.middleware.auth import get_current_user, oauth2_scheme, is_token_revoked, create_access_token
from asep.models import RefreshToken, RevokedToken, hash_refresh_token
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Body
from datetime import datetime, timedelta

app = FastAPI()



@app.get("/api/v1/projects")
def list_projects() -> list[dict]:
    # Mock projects endpoint
    return [{"id": 1, "name": "ASEP Platform", "status": "running"}]
app.include_router(api_router, prefix="/api/v1")

# Health check endpoint
@app.get("/api/v1/projects")
def list_projects(user=Depends(require_role("admin"))) -> list[dict]:
    # Mock projects endpoint, only accessible by admin users
    return [{"id": 1, "name": "ASEP Platform", "status": "running"}]

@app.post("/api/v1/logout")
def logout(
    refresh_token: str = Body(..., embed=True),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(lambda: Session.object_session(None))  # placeholder, replace with real DB session
):
    """
    Invalidate the current access token and the provided refresh token.
app.include_router(api_router, prefix="/api/v1", dependencies=[Depends(require_role("user"))])

# Health check endpoint
        db.add(revoked)

    # Revoke refresh token
    token_hash = hash_refresh_token(refresh_token)
    stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    rt = db.execute(stmt).scalar_one_or_none()
    if rt:
        rt.revoked = True
        db.add(rt)

    db.commit()
    return {"detail": "Logged out successfully"}

@app.get("/api/v1/me")
def read_current_user(payload: dict = Depends(get_current_user)):
    """Endpoint to fetch the current user's JWT payload."""
    return {"user_id": payload.get("sub"), "roles": payload.get("roles", [])}