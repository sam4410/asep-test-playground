from fastapi import FastAPI, APIRouter, HTTPException
import random
from asep.db.models import WeatherResponse

app = FastAPI()
router = APIRouter()

@router.get("/api/v1/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str):
    if not city or not all(part.replace(" ", "").isalpha() for part in city.split()) or any(part == "" for part in city.split()):
        raise HTTPException(status_code=422, detail="Invalid city name")
    
    temperature = round(random.uniform(-10, 40), 1)  # Random temperature between -10 and 40
    condition = random.choice(["sunny", "rainy", "cloudy"])  # Random weather condition
    return WeatherResponse(city=city, temperature=temperature, condition=condition)

app.include_router(router)
# Commenting out the static files mounting to prevent errors during testing
# from starlette.staticfiles import StaticFiles
# app.mount("/", StaticFiles(directory="static", html=True), name="static")  # Ensure the static directory exists # from starlette.staticfiles import StaticFiles
 # app.mount("/", StaticFiles(directory="static", html=True), name="static")  # Ensure the static directory exists