from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .config import get_settings
from .database import SessionLocal, engine

tags_metadata = [
    {
        "name": "add sensor reading",
        "description": "Add a sensor reading to the database"
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

@v1.post("/temperature/", tags=["add sensor reading"])
async def create_temperature_record(temp_reading: schemas.TemperatureReading, db: Session = Depends(get_db)):
    crud.create_temp_record(db=db, temp_reading=temp_reading)
    return 200

app.mount("/v1", v1)