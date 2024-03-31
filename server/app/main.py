from datetime import datetime, timezone
from typing import Tuple

from app import models, schemas
from app.db import SessionLocal
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lib.geocoding import get_distance_between
from lib.llm import agent_executor
from sqlalchemy.orm import Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/outlets", response_model=list[schemas.Outlet])
async def read_outlets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Outlet).offset(skip).limit(limit).all()


@app.post("/outlets/within_radius")
async def get_outlets_within_radius(
    latitude: float, longitude: float, distance: int, db: Session = Depends(get_db)
):
    outlets = db.query(models.Outlet).all()
    outlets_within_radius = []
    for outlet in outlets:
        distance_between = get_distance_between(
            (outlet.latitude, outlet.longitude), (latitude, longitude)
        )
        if distance_between > 0 and distance_between <= distance:
            outlets_within_radius.append(
                {
                    **outlet.__dict__,
                    "distance": distance_between,
                }  # hacky way to turn schema to dict using __dict__
            )
    return outlets_within_radius


@app.post("/ask")
async def ask(input: str):
    try:
        result = agent_executor.invoke(
            {
                "input": input,
                "dialect": "PostgreSQL",
                "top_k": 10,
            }
        )
        return {
            "input": input,
            "output": result["output"],
            "error": False,
            "datetime": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        return {
            "input": input,
            "output": "Internal Server Error. Please contact the admin to resolve this issue.",
            "error": True,
            "datetime": datetime.now(timezone.utc).isoformat(),
        }
