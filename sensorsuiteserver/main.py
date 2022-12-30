from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .config import get_settings
from .database import SessionLocal, engine

tags_metadata = [
    {
        "name": "sensor reading",
        "description": "Interact with sensor readings in the database"
    }
]


app = FastAPI()

v1 = FastAPI(
    title="sensorsuite-server",
    description="Server for recording and retrieving various sensor data in a database",
    version="0.0.1",
    contact={
        "name": "Bryce Jenkins",
        "url": "https://github.com/thechainercygnus/sensorsuite-server",
        "email": "bryce@durish.xyz",
    },
    openapi_tags=tags_metadata,
    docs_url=None,
    redoc_url="/",
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def raise_not_found(request):
    message = f"Endpoint '{request.url}' undefined"
    raise HTTPException(status_code=404, detail=message)

@v1.post("/temperature/", tags=["sensor reading"])
async def create_temperature_record(temp_reading: schemas.TemperatureReading, db: Session = Depends(get_db)):
    crud.create_temp_record(db=db, temp_reading=temp_reading)
    return 200

@v1.get("/temperature/", tags=["sensor reading"], response_model=list[schemas.TemperatureReading])
async def get_temperature_records(start_time: str, request: Request, db: Session = Depends(get_db), sensor_id: str | None = None):
    try:
        start_dtm = datetime.strptime(start_time, "%Y%m%dT%H%M%S")
    except:
        raise_not_found(request)
    temperature_range = crud.get_temp_records(db=db, start_time=start_dtm, sensor_id=sensor_id)
    return temperature_range

app.mount("/v1", v1)