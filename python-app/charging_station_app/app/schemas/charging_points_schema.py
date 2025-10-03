from pydantic import BaseModel
from typing import List, Optional
from app.schemas.connectors_schema import ConnectorOut

class ChargingPointCreate(BaseModel):
    code: str
    max_power_kw: int
    station_id: int


class ChargingPointOut(BaseModel):
    id: int
    code: str
    max_power_kw: int
    station_id: int
    connectors: List[ConnectorOut] = []

    class Config:
        orm_mode = True
