from fastapi import FastAPI, APIRouter
import random
from asep.db.models import WeatherResponse

app = FastAPI()
router = APIRouter()

@router.get("/api/v1/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str):
    temperature = round(random.uniform(-10, 40), 1)  # Random temperature between -10 and 40
    condition = random.choice(["sunny", "rainy", "cloudy"])  # Random weather condition
    return WeatherResponse(city=city, temperature=temperature, condition=condition)

app.include_router(router)