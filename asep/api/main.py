from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from asep.db import get_db
from asep.db.models import UserModel, RefreshTokenModel
def list_projects() -> list[dict]:
    # Mock projects endpoint
    return [{"id": 1, "name": "ASEP Platform", "status": "running"}]


class TokenResponse(BaseModel):
from asep.auth import create_access_token, create_refresh_token, verify_refresh_token
from asep.auth import get_current_user, get_current_active_user
from asep.auth import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
import os

app = FastAPI()

def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate user and issue JWT access and refresh tokens.
    """
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=access_token_expires,
    )

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=refresh_token_expires,
    )

    # Store refresh token hash for rotation
    db_refresh = RefreshTokenModel(
        token=refresh_token,
        user_id=user.id,
        expires_at=datetime.utcnow() + refresh_token_expires,
    )
    db.add(db_refresh)
    db.commit()

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@app.post("/refresh", response_model=TokenResponse)
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    """
    Rotate refresh token and issue new access token.
    """
    payload = verify_refresh_token(refresh_token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Ensure token exists and not revoked
    stored = (
        db.query(RefreshTokenModel)
        .filter(RefreshTokenModel.token == refresh_token, RefreshTokenModel.user_id == user_id)
        .first()
    )
    if not stored or stored.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired or revoked")

    # Rotate: delete old token
    db.delete(stored)
    db.commit()

    # Issue new tokens
    access_token = create_access_token(data={"sub": str(user_id)}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    new_refresh = create_refresh_token(data={"sub": str(user_id)}, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    db.add(RefreshTokenModel(token=new_refresh, user_id=user_id, expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)))
    db.commit()

    return TokenResponse(access_token=access_token, refresh_token=new_refresh)