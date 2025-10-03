from pydantic import BaseModel
from typing import Optional

class ConnectorCreate(BaseModel):
    type: str
    charging_point_id: int
    status_id: int

class ConnectorUpdateStatus(BaseModel):
    status_name: str

class ConnectorStatusOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ConnectorOut(BaseModel):
    id: int
    type: str
    charging_point_id: int
    status: ConnectorStatusOut

    class Config:
        orm_mode = True
