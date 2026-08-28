from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
from routers import feature  # Import your feature router here

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(feature.router)  # Include your feature router

@app.get("/")
def read_root():
    return {"message": "Welcome to the Freelancer Invoice Tracker API"}

# Add more routes or include additional routers as needed

# To run the app, use: uvicorn main:app --reload
# Ensure to set the environment variables for database and Clerk credentials
