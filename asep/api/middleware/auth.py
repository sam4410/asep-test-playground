import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Callable

# In a real app, use a secure secret and proper algorithms
JWT_SECRET = "your-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def decode_jwt(token: str) -> dict:
    """
    Decode a JWT token and return its payload.
    Raises HTTPException if token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_role(required_role: str) -> Callable:
    """
    Dependency that ensures the JWT contains the required role.
    Usage:
        @app.get("/admin")
        def admin_endpoint(user=Depends(require_role("admin"))):
            ...
    """
    async def role_checker(token: str = Depends(oauth2_scheme)):
        payload = decode_jwt(token)
        roles = payload.get("roles", [])
        if isinstance(roles, str):
            roles = [roles]
        if required_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return payload  # return the whole payload for downstream use if needed

    return role_checker

# Optional helper to get current user without role check
def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    return decode_jwt(token)