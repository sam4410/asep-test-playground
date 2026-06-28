"""
Authorization middleware for role‑based access control.

Provides a FastAPI dependency that ensures the current authenticated user
has the required role (e.g., "admin" or "user").  It builds on the existing
``get_current_active_user`` dependency which validates the JWT and returns a
SQLAlchemy ``UserModel`` instance.
"""

from fastapi import Depends, HTTPException, status
from asep.auth import get_current_active_user
from asep.db.models import UserModel


def require_role(required_role: str):
    """
    FastAPI dependency factory that enforces a specific user role.

    Usage::

        @app.get("/admin")
        def admin_endpoint(user: UserModel = Depends(require_role("admin"))):
            return {"msg": "Welcome admin"}

    Parameters
    ----------
    required_role: str
        The role that the user must possess. Typically ``"admin"`` or ``"user"``.

    Returns
    -------
    Depends
        A FastAPI ``Depends`` object that resolves to the current ``UserModel``
        if the role matches, otherwise raises ``HTTPException`` with 403.
    """

    async def role_checker(
        current_user: UserModel = Depends(get_current_active_user),
    ) -> UserModel:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return Depends(role_checker)