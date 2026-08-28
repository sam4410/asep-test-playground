import os
from fastapi import Request, HTTPException, Depends
from clerk_backend_api import authenticate_request, AuthenticateRequestOptions
from sqlalchemy.orm import Session
from database import get_db
from models import User

def require_user(request: Request, db: Session = Depends(get_db)) -> User:
    state = authenticate_request(
        request,
        AuthenticateRequestOptions(
            secret_key=os.environ["CLERK_SECRET_KEY"],
            authorized_parties=[os.environ.get("ALLOWED_ORIGIN", "*")],
        ),
    )
    if not state.is_signed_in:
        raise HTTPException(status_code=401, detail=state.reason.name if state.reason else "unauthorized")

    clerk_user_id = state.payload["sub"]
    user = db.query(User).filter(User.clerk_user_id == clerk_user_id).first()
    if not user:
        user = User(clerk_user_id=clerk_user_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user