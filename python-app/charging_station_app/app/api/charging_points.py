from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.charging_points_schema import ChargingPointOut, ChargingPointCreate
from app.services.charging_point_service import ChargingPointService
from app.database import get_db
from app.redis import get_redis

router = APIRouter(prefix="/charging-points", tags=["charging-points"])


@router.get("/", response_model=List[ChargingPointOut])
def list_charging_points(db: Session = Depends(get_db)):
    service = ChargingPointService(db)
    return service.list_all()

@router.post("/", response_model=ChargingPointOut, status_code=status.HTTP_201_CREATED)
def create_charging_point(cp_data: ChargingPointCreate, db: Session = Depends(get_db)):
    service = ChargingPointService(db)
    return service.create_charging_point(cp_data)

@router.delete("/{cp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_charging_point(cp_id: int, db: Session = Depends(get_db)):
    service = ChargingPointService(db)
    try:
        service.delete_charging_point(cp_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))