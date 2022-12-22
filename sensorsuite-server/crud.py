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
