import jwt
import uuid
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Callable, Optional, Dict, Any

# In a real app, use a secure secret and proper algorithms
JWT_SECRET = "your-secret-key"
    """
    from asep.models import RevokedToken
    token = db_session.query(RevokedToken).filter_by(jti=jti).first()
    return token is not None and not token.is_expired()

# Optional helper to get current user without role check
def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def _generate_jti() -> str:
    """
    Generate a unique JWT ID (jti) for token revocation tracking.
    """
    return str(uuid.uuid4())

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
    roles: Optional[list[str]] = None,
) -> str:
    """
    Create a signed JWT access token.
    - ``data``: payload data (e.g., ``{\"sub\": user_id}``).
    - ``expires_delta``: optional custom expiry, defaults to 15 minutes.
    - ``roles``: optional list of role strings to embed in the token.
    Returns the encoded JWT string.
    """
    to_encode = data.copy()
    now = datetime.utcnow()
    expire = now + (expires_delta or timedelta(minutes=15))
    to_encode.update(
        {"exp": expire, "iat": now, "jti": _generate_jti(), "roles": roles or []}
    )
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def require_role(required_role: str) -> Callable:
