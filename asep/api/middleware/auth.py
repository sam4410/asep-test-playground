"""
Role based access control middleware for the ASEP FastAPI backend.

The `require_role` function returns a FastAPI dependency that can be used
in endpoint definitions to enforce that the caller possesses one of the
allowed roles.  The role is expected to be supplied via the request
header ``X-User-Role`` – this mirrors the simple JWT‑based auth that will
be added later in the project.

Example usage:

```python
from fastapi import APIRouter, Depends
from asep.api.middleware import require_role

router = APIRouter()

@router.get("/admin")
def admin_endpoint(role: str = Depends(require_role("Manager", "Executive"))):
    return {"msg": f"Welcome, {role}!"}
```

If the header is missing or the role is not in the allowed list, a
``403 Forbidden`` response is returned.
"""

from typing import Callable, Iterable

from fastapi import Header, HTTPException, Request, status


def _extract_role(x_user_role: str | None = Header(default=None, alias="X-User-Role")) -> str:
    """
    Helper that extracts the role from the request header.
    Raises a 401 if the header is missing.
    """
    if not x_user_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-User-Role header",
        )
    return x_user_role


def require_role(*allowed_roles: str) -> Callable[[Request], str]:
    """
    FastAPI dependency that enforces the caller's role.

    Parameters
    ----------
    *allowed_roles: str
        One or more role names that are permitted to access the endpoint.

    Returns
    -------
    Callable[[Request], str]
        A dependency function that returns the validated role string.
    """

    if not allowed_roles:
        raise ValueError("At least one role must be specified for require_role")

    allowed_set: set[str] = set(allowed_roles)

    async def dependency(request: Request, role: str = Header(default=None, alias="X-User-Role")) -> str:
        # FastAPI will inject the header value; we perform validation here.
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing X-User-Role header",
            )
        if role not in allowed_set:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role}' does not have permission for this resource",
            )
        # Return the role so endpoint functions can optionally use it.
        return role

    return dependency

