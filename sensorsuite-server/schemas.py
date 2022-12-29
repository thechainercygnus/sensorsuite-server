from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class SensorReadingBase(BaseModel):
    sensor_id: str
    timestamp: datetime | None = None

class TemperatureReading(SensorReadingBase):
    temperature_c: float
    humidity: float

    class Config:
        orm_mode = True