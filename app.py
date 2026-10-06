from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables
from routers.todos import router as todos_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(todos_router)
