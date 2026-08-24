from fastapi import FastAPI, HTTPException
from fastapi import APIRouter
from sqlalchemy.orm import Session
from asep.db.models import Note
from asep.db.database import SessionLocal, engine
from pydantic import BaseModel
from datetime import datetime

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
    return db_note

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)