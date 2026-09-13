from fastapi import FastAPI

from app.routers.habits import router as habits_router


def create_app() -> FastAPI:
    application = FastAPI(title="Daily Habit Tracker")
    application.include_router(habits_router)
    return application


app = create_app()
