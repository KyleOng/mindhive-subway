import sys
from pathlib import Path

# Add the parent directory of the current file to the system path
# This allows accessing methods defined in subdirectories of the parent directory.
sys.path.append(str(Path(__file__).parent.parent))

from datetime import datetime, timezone

import uvicorn
from api import models, schemas
from api.db import SessionLocal
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


# nginx proxy
app = FastAPI(root_path="/api") 


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"liveness": "ok"}


@app.get("/outlets", response_model=list[schemas.Outlet])
async def read_outlets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Outlet).offset(skip).limit(limit).all()


@app.post("/outlets/operating_hours")
async def get_operating_hours(outlet_id: int, db: Session = Depends(get_db)):
    return db.query(models.OperatingHour).where(models.OperatingHour.outlet_id == outlet_id).all()


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


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)
