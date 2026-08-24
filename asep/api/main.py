from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from asep.api.quizzes import router as quizzes_router
from asep.api.main import app  # Corrected import statement to reflect the correct module path

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")