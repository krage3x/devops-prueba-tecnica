from pydantic import BaseModel
from typing import Optional
from app.schemas.connectors_status_schema import ConnectorStatusOut  

class ConnectorCreate(BaseModel):
    type: str
    charging_point_id: int
    status_id: int

class ConnectorUpdateStatus(BaseModel):
    status_name: str


class ConnectorCreate(BaseModel):
    type: str
    charging_point_id: int
    status_id: int

class ConnectorUpdateStatus(BaseModel):
    status_name: str


class ConnectorOut(BaseModel):
    id: int
    type: str
    charging_point_id: int
    status: ConnectorStatusOut 
    model_config = {"from_attributes": True}