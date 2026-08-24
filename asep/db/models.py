from pydantic import BaseModel

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    condition: str

    class Config:
        schema_extra = {
            "example": {
                "city": "London",
                "temperature": 22.5,
                "condition": "sunny"
            }
        }
