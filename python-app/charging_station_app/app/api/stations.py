from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.stations_schema import StationOut, StationCreate
from app.services.station_service import StationService
from app.database import get_db
from app.redis import get_redis

router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("/", response_model=List[StationOut])
def list_stations(db: Session = Depends(get_db)):
    service = StationService(db)
    return service.list_stations()


@router.post("/", response_model=StationOut, status_code=status.HTTP_201_CREATED)
def create_station(station_data: StationCreate, db: Session = Depends(get_db)):
    service = StationService(db)
    return service.create_station(station_data)


@router.delete("/{station_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_station(station_id: int, db: Session = Depends(get_db)):
    service = StationService(db)
    try:
        service.delete_station(station_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))