from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List

from app.recommender import generate_recommendations


app = FastAPI(title="GT7 AI Settings Assistant")


class RecommendationRequest(BaseModel):
    car: str = Field(..., min_length=2)
    track: str = Field(..., min_length=2)
    weather: str = Field(default="clear")
    time_of_day: str = Field(default="day")
    custom_parts: List[str] = Field(default_factory=list)
    struggles: List[str] = Field(default_factory=list)


@app.get("/")
def index():
    return FileResponse("app/static/index.html")


@app.post("/api/recommend")
def recommend(payload: RecommendationRequest):
    return generate_recommendations(
        car=payload.car,
        track=payload.track,
        weather=payload.weather,
        time_of_day=payload.time_of_day,
        custom_parts=payload.custom_parts,
        struggles=payload.struggles,
    )


app.mount("/app/static", StaticFiles(directory="app/static"), name="static")
