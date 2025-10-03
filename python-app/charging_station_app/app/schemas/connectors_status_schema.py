from pydantic import BaseModel
from typing import List, Optional

class ConnectorStatusCreate(BaseModel):
    name: str


class ConnectorStatusOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
