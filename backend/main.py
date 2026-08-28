from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import invoices  # Import the invoices router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(invoices.router)  # Include the invoices router

@app.get("/")
def read_root():
    return {"message": "Welcome to the Freelancer Invoice Tracker API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run the app on port 8000
