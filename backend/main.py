from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, habits

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(habits.router, prefix="/habits", tags=["habits"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Habit Tracker API!"}