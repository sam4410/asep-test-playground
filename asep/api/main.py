from fastapi import FastAPI, HTTPException
from fastapi import APIRouter
from sqlalchemy.orm import Session
from asep.db.models import Note
from asep.db.database import SessionLocal, engine
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI()
router = APIRouter()

class NoteCreate(BaseModel):
    title: str
    body: str

@router.post("/api/v1/notes", response_model=Note)
def create_note(note: NoteCreate):
    db: Session = SessionLocal()
    db_note = Note(title=note.title, body=note.body)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return {
        "id": db_note.id,
        "title": db_note.title,
        "body": db_note.body,
        "created_at": db_note.created_at.isoformat()
    }

if os.path.exists("static") and os.path.isdir("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)@app.on_event("startup")