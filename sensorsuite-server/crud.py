from sqlalchemy.orm import Session

from . import models, schemas


def create_temp_record(db: Session, temp_reading: schemas.TemperatureReading) -> models.Temperature:
    db_temperature = models.Temperature(
        sensor_id = temp_reading.sensor_id,
        temperature_c = temp_reading.temperature_c,
        humidity = temp_reading.humidity,
    )   
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

def get_temp_records(db: Session, start_time: str, sensor_id: str | None = None) -> schemas.TemperatureReading:
    if sensor_id is None:
        return (
            db.query(models.Temperature)
            .filter(models.Temperature.created_at >= start_time)
        )