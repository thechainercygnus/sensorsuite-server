from . import models, schemas

def to_schema(model: models.Temperature) -> schemas.TemperatureReading:
    return schemas.TemperatureReading(
        sensor_id=model.sensor_id,
        timestamp=model.created_at,
        temperature_c=model.temperature_c,
        humidity=model.humidity
    )