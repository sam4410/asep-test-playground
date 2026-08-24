import os  # Ensure the static directory exists
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from asep.api import questions, auth, expenses, tasks

if not os.path.exists("static"):
    os.makedirs("static")  # Create the static directory if it does not exist

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="static")