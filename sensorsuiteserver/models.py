from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Float

from .database import Base


class Temperature(Base):
    __tablename__ = "Temperatures"

    id = Column(Integer, primary_key=True)
    sensor_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    temperature_c = Column(Float)
    humidity = Column(Float)