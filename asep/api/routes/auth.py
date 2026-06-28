"""
Authentication routes for FastAPI.
Provides a `/refresh` endpoint that validates a stored refresh token,
rotates it, and returns a new access token (and a new refresh token).

NOTE: This is a minimal implementation using an in‑memory store.
In production you would persist refresh tokens in a database,
use secure random secrets, and rotate secrets via environment variables.
"""

import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any

import jwt
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from ..middleware.auth import JWT_SECRET, ALGORITHM, decode_jwt

router = APIRouter()

# In‑memory store for refresh tokens: token -> {"user_id": ..., "expires": ...}
_refresh_store: Dict[str, Dict[str, Any]] = {}

# Token lifetimes
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

def _create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

def _create_refresh_token(user_id: str) -> str:
    token = str(uuid.uuid4())
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    _refresh_store[token] = {"user_id": user_id, "expires": expire}
    return token

def _verify_refresh_token(token: str) -> str:
    """
    Verify that the refresh token exists and has not expired.
    Returns the associated user_id if valid, otherwise raises HTTPException.
    """
    entry = _refresh_store.get(token)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    if entry["expires"] < datetime.utcnow():
        # Remove expired token
        _refresh_store.pop(token, None)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
        )
    return entry["user_id"]

def _rotate_refresh_token(old_token: str, user_id: str) -> str:
    """
    Remove the old refresh token and issue a new one.
    """
    _refresh_store.pop(old_token, None)
    return _create_refresh_token(user_id)

@router.post("/refresh")
def refresh_token(refresh_token: str):
    """
    Refresh endpoint.
    Expects JSON body: { "refresh_token": "<token>" }
    Returns new access and refresh tokens.
    """
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token required",
        )

    # Validate and retrieve user identity
    user_id = _verify_refresh_token(refresh_token)

    # Create new tokens
    access_payload = {"sub": user_id, "roles": ["user"]}  # roles could be fetched from DB
    new_access = _create_access_token(access_payload)
    new_refresh = _rotate_refresh_token(refresh_token, user_id)

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "bearer",
    }

# Expose a helper to generate initial tokens (e.g., after login)
def generate_initial_tokens(user_id: str, roles: list) -> dict:
    """
    Utility used by the login endpoint to issue the first pair of tokens.
    """
    access_payload = {"sub": user_id, "roles": roles}
    access_token = _create_access_token(access_payload)
    refresh_token = _create_refresh_token(user_id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }