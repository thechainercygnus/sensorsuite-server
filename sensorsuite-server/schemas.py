from typing import Optional

from pydantic import BaseModel


class SensorReadingBase(BaseModel):
    sensor_id: str
    timestamp: int


class TemperatureReading(SensorReadingBase):
    temperature_c: float
    humidity: float

    class Config:
        orm_mode = True