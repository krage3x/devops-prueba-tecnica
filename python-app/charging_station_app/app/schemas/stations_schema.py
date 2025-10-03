from pydantic import BaseModel
from typing import List, Optional
from app.schemas.charging_points_schema import ChargingPointOut

class StationCreate(BaseModel):
    name: str
    location: str

class StationOut(BaseModel):
    id: int
    name: str
    location: str
    charging_points: List[ChargingPointOut] = []

    class Config:
        orm_mode = True
