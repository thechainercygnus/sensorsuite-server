from datetime import datetime

from sqlalchemy.orm import Session

from . import models, schemas, transformers


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

def get_temp_records(db: Session, start_time: datetime, sensor_id: str | None = None) -> schemas.TemperatureReading:
    if sensor_id is None:
        temp_models = (
            db.query(models.Temperature)
            .filter(models.Temperature.created_at >= start_time)
        )
    else:
        temp_models = (
            db.query(models.Temperature)
            .filter(models.Temperature.created_at >= start_time, models.Temperature.sensor_id == sensor_id)
        )
    return_temps = []
    for model in temp_models:
        return_temps.append(transformers.to_schema(model=model))
    return return_temps