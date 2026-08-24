from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from asep.api.routes import router

app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")  # Uncomment if static files are needed