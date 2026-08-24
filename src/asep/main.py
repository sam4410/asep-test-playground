from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
import os

app = FastAPI()

static_directory = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_directory):
    os.makedirs(static_directory)

app.mount("/", StaticFiles(directory=static_directory, html=True), name="static")