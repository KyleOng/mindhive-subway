from sqlalchemy import (
    Column,
    Integer,
    String,
    Time,
    ForeignKey,
    TIMESTAMP,
    DECIMAL,
    func,
)
from sqlalchemy.orm import relationship

from .db import Base


class Outlet(Base):
    __tablename__ = "outlets"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    waze_link = Column(String)
    longitude = Column(DECIMAL, default=0)
    latitude = Column(DECIMAL, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    operating_hours = relationship("OperatingHour", back_populates="outlet")

    def __repr__(self):
        return f"Outlet(id={self.id}, name='{self.name}', address='{self.address}', waze_link='{self.waze_link}')"


class OperatingHour(Base):
    __tablename__ = "operating_hours"

    id = Column(Integer, primary_key=True)
    outlet_id = Column(Integer, ForeignKey("outlets.id"))
    day_of_the_week = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    outlet = relationship("Outlet", back_populates="operating_hours")

    def __repr__(self):
        return f"OperatingHour(id={self.id}, outlet_id={self.outlet_id}, day_of_the_week='{self.day_of_the_week}', start_time='{self.start_time}', end_time='{self.end_time}')"
