from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import models, schemas
from .db import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/outlets", response_model=list[schemas.Outlet])
async def read_outlets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Outlet).offset(skip).limit(limit).all()


@app.post("/outlet", response_model=schemas.Outlet)
async def create_outlet(outlet: schemas.OutletCreate, db: Session = Depends(get_db)):
    db_outlet = models.Outlet(
        name=outlet.name,
        address=outlet.address,
        waze_link=outlet.waze_link,
        longitude=outlet.longitude,
        latitude=outlet.latitude,
    )
    db.add(db_outlet)
    db.commit()
    db.refresh(db_outlet)
    return db_outlet
