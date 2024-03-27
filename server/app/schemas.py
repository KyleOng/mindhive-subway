from pydantic import BaseModel
from datetime import datetime, time


class OutletBase(BaseModel):
    name: str
    address: str
    waze_link: str
    longitude: float = 0
    latitude: float = 0


class OutletCreate(OutletBase):
    pass


class Outlet(OutletBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class OperatingHourBase(BaseModel):
    day_of_the_week: str
    start_time: time
    end_time: time


class OperatingHourCreate(OperatingHourBase):
    pass


class OperatingHour(OperatingHourBase):
    outlets: list[Outlet] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
