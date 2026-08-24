from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
import os

app = FastAPI()

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir) and os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
else:
    print(f"Warning: Static directory '{static_dir}' does not exist. Static files will not be served.")