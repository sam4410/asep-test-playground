import os

os.makedirs("static", exist_ok=True)  # Ensure the 'static' directory exists
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from asep.api.quizzes import router as quizzes_router
from asep.api.main import app  # Corrected import statement to reflect the correct module path

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")
app = FastAPI()

static_dir = "static"
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")