from fastapi import FastAPI, Depends
from .db import SessionLocal, engine
from sqlalchemy.orm import Session
from . import models, schemas


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/outlets", response_model=list[schemas.Outlet])
async def read_outlets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Outlet).offset(skip).limit(limit).all()
